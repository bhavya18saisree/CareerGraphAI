from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from navigator.recommendation import get_career_recommendations
from navigator.skill_gap import get_skill_gap
from navigator.learning_path import get_learning_path
from navigator.multi_hop import get_multi_hop_recommendations


# =========================================
# HOME PAGE
# =========================================

def home(request):
    return render(request, "index.html")


# =========================================
# CAREER RECOMMENDATION
# =========================================

@csrf_exempt
def career_recommendation(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "Only POST requests are allowed"
            },
            status=405
        )

    try:

        data = json.loads(
            request.body.decode("utf-8")
        )

        user_skills = data.get("skills", [])

        if not user_skills:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Please select at least one skill."
                },
                status=400
            )

        recommendations = get_career_recommendations(
            user_skills
        )

        return JsonResponse(
            {
                "success": True,
                "skills": user_skills,
                "recommendations": recommendations
            }
        )

    except Exception as e:

        print("Career recommendation error:", e)

        return JsonResponse(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )


# =========================================
# SKILL GAP
# =========================================

@csrf_exempt
def skill_gap(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "Only POST requests are allowed"
            },
            status=405
        )

    try:

        data = json.loads(
            request.body.decode("utf-8")
        )

        user_skills = data.get(
            "skills",
            []
        )

        career = data.get(
            "career",
            ""
        )

        if not career:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Career is required"
                },
                status=400
            )

        result = get_skill_gap(
            user_skills,
            career
        )

        return JsonResponse(
            {
                "success": True,
                "skills": user_skills,
                "career": career,
                "result": result
            }
        )

    except Exception as e:

        print("Skill gap error:", e)

        return JsonResponse(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )


# =========================================
# LEARNING PATH
# =========================================

@csrf_exempt
def learning_path(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "Only POST requests are allowed"
            },
            status=405
        )

    try:

        data = json.loads(
            request.body.decode("utf-8")
        )

        user_skills = data.get(
            "skills",
            []
        )

        career = data.get(
            "career",
            ""
        )

        if not career:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Career is required"
                },
                status=400
            )

        result = get_learning_path(
            user_skills,
            career
        )

        return JsonResponse(
            {
                "success": True,
                "career": career,
                "learning_path": result
            }
        )

    except Exception as e:

        print("Learning path error:", e)

        return JsonResponse(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )


# =========================================
# MULTI-HOP RECOMMENDATION
# =========================================

@csrf_exempt
def multi_hop(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "error": "Only POST requests are allowed"
            },
            status=405
        )

    try:

        data = json.loads(
            request.body.decode("utf-8")
        )

        user_skills = data.get(
            "skills",
            []
        )

        if not user_skills:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Please select at least one skill."
                },
                status=400
            )

        results = get_multi_hop_recommendations(
            user_skills
        )

        return JsonResponse(
            {
                "success": True,
                "skills": user_skills,
                "multi_hop_results": results
            }
        )

    except Exception as e:

        print("Multi-hop error:", e)

        return JsonResponse(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )
