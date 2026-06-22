import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import ORO_AGE_CAT, ORO_COMPS, OROSystemSettings, Registration, teams

ORO_COMP_KEYS = {key for key, _ in ORO_COMPS}
ORO_COMP_KEYS_ORDERED = [key for key, _ in ORO_COMPS]
ORO_CATEGORY_KEYS = {key for key, _ in ORO_AGE_CAT}
ORO_COMP_LABELS = {key: label for key, label in ORO_COMPS}
TEMPLATE_COMP_KEY_ALIASES = {
    "linefollower": "line_follower",
    "smartcity": "smart_city",
    "coding": "coding_mission",
}
TEMPLATE_CATEGORY_PATTERN = re.compile(r"^oro_(poussins|juniors|colleges|seniors)_(.+)\.html$")
SCORE_PATTERN = re.compile(r"Final score:\s*([0-9]+(?:\.[0-9]+)?)%")
C_GRADER_DIR = Path(__file__).resolve().parent.parent / "static" / "assets" / "img" / "oro" / "c-grader"
C_GRADER_SCRIPT = C_GRADER_DIR / "c_grader.py"
C_GRADER_REFERENCE = C_GRADER_DIR / "reference.c"
C_GRADER_SPEC = C_GRADER_DIR / "spec.json"


def _build_category_competitions():
    template_dir = Path(__file__).resolve().parent.parent / "templates"
    by_category_seen = {category_key: set() for category_key, _ in ORO_AGE_CAT}

    for template_file in sorted(template_dir.glob("oro_*_*.html")):
        match = TEMPLATE_CATEGORY_PATTERN.match(template_file.name)
        if not match:
            continue

        category_key, raw_comp_key = match.groups()
        comp_key = TEMPLATE_COMP_KEY_ALIASES.get(raw_comp_key, raw_comp_key)
        by_category_seen[category_key].add(comp_key)

    by_category = {}
    for category_key, _ in ORO_AGE_CAT:
        comp_set = by_category_seen[category_key]
        if not comp_set:
            by_category[category_key] = list(ORO_COMP_KEYS_ORDERED)
            continue

        ordered = [comp_key for comp_key in ORO_COMP_KEYS_ORDERED if comp_key in comp_set]
        extras = sorted(comp_key for comp_key in comp_set if comp_key not in ORO_COMP_KEYS)
        by_category[category_key] = ordered + extras

    return by_category


CATEGORY_COMP_KEYS = _build_category_competitions()


def _competition_label(comp_key):
    return ORO_COMP_LABELS.get(comp_key, comp_key.replace("_", " ").title())


def _is_coding_grader_released():
    return OROSystemSettings.get_solo().coding_grader_released


def _detect_missing_compiler(report: str) -> bool:
    lowered = report.lower()
    return (
        "filenotfounderror" in lowered
        and ("winerror 2" in lowered or "no such file or directory" in lowered)
        and "gcc" in lowered
    )


def oro_home(request):
    return render(request, 'oro.html')


# ORO category pages

def oro_poussins(request):
    return render(request, 'oro_poussins.html')


def oro_juniors(request):
    return render(request, 'oro_juniors.html')


def oro_colleges(request):
    return render(request, 'oro_colleges.html')


def oro_seniors(request):
    return render(request, 'oro_seniors.html')


# ORO competition pages - Poussins

def oro_poussins_bowling(request):
    return render(request, 'oro_poussins_bowling.html')


def oro_poussins_robofoot(request):
    return render(request, 'oro_poussins_robofoot.html')


def oro_poussins_smartcity(request):
    return render(request, 'oro_poussins_smartcity.html')


# ORO competition pages - Juniors

def oro_juniors_bowling(request):
    return render(request, 'oro_juniors_bowling.html')


def oro_juniors_robofoot(request):
    return render(request, 'oro_juniors_robofoot.html')


def oro_juniors_smartcity(request):
    return render(request, 'oro_juniors_smartcity.html')


# ORO competition pages - Colleges

def oro_colleges_linefollower(request):
    return render(request, 'oro_colleges_linefollower.html')


def oro_colleges_smartcity(request):
    return render(request, 'oro_colleges_smartcity.html')


def oro_colleges_sumo(request):
    return render(request, 'oro_colleges_sumo.html')


def oro_colleges_roborace(request):
    return render(request, 'oro_colleges_roborace.html')


def oro_colleges_robofoot(request):
    return render(request, 'oro_colleges_robofoot.html')


def oro_colleges_maze(request):
    return render(request, 'oro_colleges_maze.html')


def oro_colleges_firefighting(request):
    return render(request, 'oro_colleges_firefighting.html')


# ORO competition pages - Seniors

def oro_seniors_linefollower(request):
    return render(request, 'oro_seniors_linefollower.html')


def oro_seniors_smartcity(request):
    return render(request, 'oro_seniors_smartcity.html')


def oro_seniors_sumo(request):
    return render(request, 'oro_seniors_sumo.html')


def oro_seniors_coding(request):
    return render(
        request,
        'oro_seniors_coding.html',
        {"coding_grader_released": _is_coding_grader_released()},
    )


@require_POST
def oro_seniors_coding_grade(request):
    if not _is_coding_grader_released():
        return JsonResponse({"error": "Coding Mission grader is not released yet."}, status=403)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    code = str(data.get("code", ""))
    if not code.strip():
        return JsonResponse({"error": "Please provide your C source code."}, status=400)
    if len(code) > 200_000:
        return JsonResponse({"error": "Source code is too large."}, status=400)
    if shutil.which("gcc") is None:
        return JsonResponse(
            {
                "error": (
                    "C compiler not found on server. Install GCC and ensure it is in PATH "
                    "(for Windows: MinGW-w64/MSYS2 with gcc available in terminal)."
                )
            },
            status=503,
        )

    missing = [
        str(path.name)
        for path in (C_GRADER_SCRIPT, C_GRADER_REFERENCE, C_GRADER_SPEC)
        if not path.exists()
    ]
    if missing:
        return JsonResponse(
            {"error": f"Grader files are missing: {', '.join(missing)}"},
            status=500,
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        student_src = Path(tmpdir) / "student_submission.c"
        student_src.write_text(code, encoding="utf-8")

        cmd = [
            sys.executable,
            str(C_GRADER_SCRIPT),
            str(student_src),
            str(C_GRADER_REFERENCE),
            str(C_GRADER_SPEC),
        ]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            return JsonResponse({"error": "Grading timed out. Try simplifying your code."}, status=408)

    report = (proc.stdout or "")
    if proc.stderr:
        report = f"{report}\n{proc.stderr}" if report else proc.stderr
    report = report.strip()
    if len(report) > 16000:
        report = f"{report[:16000]}\n\n... output truncated ..."

    score = None
    match = SCORE_PATTERN.search(report)
    if match:
        score = float(match.group(1))

    if proc.returncode != 0 and score is None:
        if _detect_missing_compiler(report):
            return JsonResponse(
                {
                    "error": (
                        "C compiler not found on server. Install GCC and ensure it is in PATH "
                        "(for Windows: MinGW-w64/MSYS2 with gcc available in terminal)."
                    ),
                    "report": report,
                },
                status=503,
            )
        return JsonResponse(
            {"error": "Grader failed to run correctly.", "report": report},
            status=500,
        )

    return JsonResponse(
        {
            "score": score if score is not None else 0.0,
            "report": report,
        }
    )


def oro_seniors_roborace(request):
    return render(request, 'oro_seniors_roborace.html')


def oro_seniors_maze(request):
    return render(request, 'oro_seniors_maze.html')


def oro_seniors_firefighting(request):
    return render(request, 'oro_seniors_firefighting.html')


def oro_dashboard_login(request):
    next_url = (request.GET.get("next") or request.POST.get("next") or "").strip()
    if not next_url or not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = "oro_dashboard"

    if request.user.is_authenticated and request.user.is_staff:
        return redirect(next_url)

    error = ""
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is None:
            error = "Invalid username or password."
        elif not user.is_staff:
            error = "This account is not allowed to modify the dashboard."
        else:
            login(request, user)
            return redirect(next_url)

    return render(request, "oro_dashboard_login.html", {
        "error": error,
        "next": next_url,
    })


@require_POST
def oro_release_coding_grader(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("oro_dashboard_login")

    settings_obj = OROSystemSettings.get_solo()
    settings_obj.coding_grader_released = not settings_obj.coding_grader_released
    settings_obj.save(update_fields=["coding_grader_released"])
    return redirect("oro_dashboard")


@require_POST
def oro_dashboard_logout(request):
    logout(request)
    return redirect("oro_dashboard_login")


def _build_dashboard_payload():
    category_labels = {key: label for key, label in ORO_AGE_CAT}

    grouped = defaultdict(lambda: defaultdict(lambda: {"scores": defaultdict(int), "total": 0}))
    score_rows = (
        teams.objects.values("category", "team_name", "competition")
        .annotate(score_sum=Sum("score"))
        .order_by()
    )

    for row in score_rows:
        category_key = row["category"]
        team_name = row["team_name"]
        competition_key = row["competition"]
        score_value = row["score_sum"] or 0

        team_bucket = grouped[category_key][team_name]
        team_bucket["scores"][competition_key] += score_value
        team_bucket["total"] += score_value

    categories = []
    for category_key, category_label in ORO_AGE_CAT:
        teams_for_category = []
        team_map = grouped.get(category_key, {})
        category_comp_keys = CATEGORY_COMP_KEYS.get(category_key, ORO_COMP_KEYS_ORDERED)
        category_competitions = [
            {"key": comp_key, "label": _competition_label(comp_key)}
            for comp_key in category_comp_keys
        ]

        for team_name, info in team_map.items():
            normalized_scores = {
                comp_key: int(info["scores"].get(comp_key, 0)) for comp_key in category_comp_keys
            }
            teams_for_category.append(
                {
                    "team_name": team_name,
                    "scores": normalized_scores,
                    "total": int(info["total"]),
                }
            )

        teams_for_category.sort(key=lambda item: (-item["total"], item["team_name"].lower()))
        previous_total = None
        previous_rank = 0
        for index, team_row in enumerate(teams_for_category, start=1):
            if team_row["total"] == previous_total:
                team_row["rank"] = previous_rank
            else:
                team_row["rank"] = index
                previous_rank = index
                previous_total = team_row["total"]

        categories.append(
            {
                "key": category_key,
                "label": category_labels.get(category_key, category_key.title()),
                "competitions": category_competitions,
                "teams": teams_for_category,
            }
        )

    return {
        "categories": categories,
        "updated_at": timezone.now().isoformat(),
    }


def oro_dashboard(request):
    return render(request, "oro_dashboard.html", {
        "dashboard_data": _build_dashboard_payload(),
        "is_staff": request.user.is_staff,
        "coding_grader_released": _is_coding_grader_released(),
    })


def oro_dashboard_data(request):
    return JsonResponse(_build_dashboard_payload())


@require_POST
def score_update(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Forbidden"}, status=403)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    team_name = data.get("team_name", "").strip()
    category = data.get("category", "").strip()
    competition = data.get("competition", "").strip()
    try:
        score = int(data.get("score", 0))
        if score < 0:
            raise ValueError
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid score"}, status=400)

    if not (team_name and category and competition):
        return JsonResponse({"error": "Missing fields"}, status=400)
    if category not in ORO_CATEGORY_KEYS:
        return JsonResponse({"error": "Invalid category"}, status=400)
    if competition not in ORO_COMP_KEYS:
        return JsonResponse({"error": "Invalid competition"}, status=400)
    if competition not in CATEGORY_COMP_KEYS.get(category, ORO_COMP_KEYS_ORDERED):
        return JsonResponse({"error": "Competition is not valid for this category"}, status=400)

    with transaction.atomic():
        qs = teams.objects.select_for_update().filter(
            team_name=team_name,
            category=category,
            competition=competition,
        )
        first = qs.first()
        if first:
            qs.exclude(pk=first.pk).delete()
            first.score = score
            first.save(update_fields=["score"])
        else:
            sibling = teams.objects.select_for_update().filter(team_name=team_name, category=category).first()
            teams.objects.create(
                team_name=team_name,
                category=category,
                competition=competition,
                score=score,
                team_members_number=sibling.team_members_number if sibling else 1,
                rank=None,
            )

    return JsonResponse(_build_dashboard_payload())


@require_POST
def team_add(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Forbidden"}, status=403)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    team_name = data.get("team_name", "").strip()
    category = data.get("category", "").strip()
    try:
        members = max(1, int(data.get("members", 1)))
    except (ValueError, TypeError):
        members = 1

    if not (team_name and category):
        return JsonResponse({"error": "Missing fields"}, status=400)
    if category not in ORO_CATEGORY_KEYS:
        return JsonResponse({"error": "Invalid category"}, status=400)

    if teams.objects.filter(team_name=team_name, category=category).exists():
        return JsonResponse({"error": "Team already exists in this category"}, status=400)

    category_comp_keys = CATEGORY_COMP_KEYS.get(category, ORO_COMP_KEYS_ORDERED)
    if not category_comp_keys:
        return JsonResponse({"error": "No competitions configured for this category"}, status=400)

    teams.objects.bulk_create([
        teams(
            team_name=team_name,
            category=category,
            competition=comp_key,
            score=0,
            team_members_number=members,
            rank=None,
        )
        for comp_key in category_comp_keys
    ])

    return JsonResponse(_build_dashboard_payload())


@require_POST
def team_update(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Forbidden"}, status=403)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    category = str(data.get("category", "")).strip()
    current_team_name = str(data.get("team_name", "")).strip()
    new_team_name = str(data.get("new_team_name", "")).strip()
    scores = data.get("scores", {})

    if not (category and current_team_name and new_team_name):
        return JsonResponse({"error": "Missing fields"}, status=400)
    if category not in ORO_CATEGORY_KEYS:
        return JsonResponse({"error": "Invalid category"}, status=400)
    if not isinstance(scores, dict):
        return JsonResponse({"error": "Invalid scores payload"}, status=400)

    parsed_scores = {}
    category_comp_keys = CATEGORY_COMP_KEYS.get(category, ORO_COMP_KEYS_ORDERED)
    for comp_key in category_comp_keys:
        raw_score = scores.get(comp_key, 0)
        try:
            score = int(raw_score)
            if score < 0:
                raise ValueError
        except (ValueError, TypeError):
            return JsonResponse({"error": f"Invalid score for {comp_key}"}, status=400)
        parsed_scores[comp_key] = score

    with transaction.atomic():
        team_rows = list(
            teams.objects.select_for_update().filter(
                team_name=current_team_name,
                category=category,
            )
        )
        if not team_rows:
            return JsonResponse({"error": "Team not found"}, status=404)

        if new_team_name != current_team_name and teams.objects.filter(
            team_name=new_team_name,
            category=category,
        ).exists():
            return JsonResponse(
                {"error": "Another team with this name already exists in this category"},
                status=400,
            )

        members = team_rows[0].team_members_number
        by_competition = {}
        for row in team_rows:
            if row.competition not in by_competition:
                by_competition[row.competition] = row
            else:
                row.delete()

        for comp_key in category_comp_keys:
            row = by_competition.get(comp_key)
            if row:
                row.team_name = new_team_name
                row.score = parsed_scores[comp_key]
                row.save(update_fields=["team_name", "score"])
            else:
                teams.objects.create(
                    team_name=new_team_name,
                    category=category,
                    competition=comp_key,
                    score=parsed_scores[comp_key],
                    team_members_number=members,
                    rank=None,
                )

        teams.objects.filter(team_name=current_team_name, category=category).update(
            team_name=new_team_name
        )

    return JsonResponse(_build_dashboard_payload())


def registration(request):
    competition = request.GET.get('competition', '')

    if request.method == 'POST':
        Registration.objects.create(
            competition=request.POST.get('competition', ''),
            name=request.POST.get('name'),
            mail=request.POST.get('mail'),
            age=request.POST.get('age'),
            city=request.POST.get('city'),
            atastian=request.POST.get('atastian') == 'on',
            club=request.POST.get('club', ''),
            categorie=request.POST.get('categorie', ''),
            project_title=request.POST.get('project_title', ''),
            project_desc=request.POST.get('project_desc', ''),
            team=request.POST.get('team') == 'on',
            teammates=request.POST.get('teammates', ''),
        )
        return render(
            request,
            'registration.html',
            {'success': True, 'competition': request.POST.get('competition', '')},
        )

    return render(request, 'registration.html', {'competition': competition})
