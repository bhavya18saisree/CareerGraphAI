from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from navigator.recommendation import get_career_recommendations
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

        print(
            "Career recommendation error:",
            str(e)
        )

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

        # -----------------------------------------
        # READ REQUEST DATA
        # -----------------------------------------

        data = json.loads(
            request.body.decode("utf-8")
        )

        user_skills = data.get(
            "skills",
            []
        )

        career = str(
            data.get(
                "career",
                ""
            )
        ).strip()

        # -----------------------------------------
        # VALIDATE SKILLS
        # -----------------------------------------

        if not user_skills:

            return JsonResponse(
                {
                    "success": False,
                    "error": "Please select at least one skill."
                },
                status=400
            )

        # -----------------------------------------
        # VALIDATE CAREER
        # -----------------------------------------

        if not career:

            return JsonResponse(
                {
                    "success": False,
                    "error": "Career is required"
                },
                status=400
            )

        # -----------------------------------------
        # USE SAME ENGINE AS STEP 02
        # -----------------------------------------

        recommendations = get_career_recommendations(
            user_skills
        )

        print("-----------------------------------------")
        print("SKILL GAP REQUEST")
        print("User skills:", user_skills)
        print("Selected career:", career)
        print("Recommendations:", recommendations)
        print("-----------------------------------------")

        # -----------------------------------------
        # FIND SELECTED CAREER
        # -----------------------------------------

        selected_result = None

        for recommendation in recommendations:

            recommendation_career = str(
                recommendation.get(
                    "career",
                    ""
                )
            ).strip()

            if (
                recommendation_career.lower()
                ==
                career.lower()
            ):

                selected_result = recommendation
                break

        # -----------------------------------------
        # CAREER NOT FOUND
        # -----------------------------------------

        if selected_result is None:

            return JsonResponse(
                {
                    "success": False,
                    "error": "Selected career was not found.",
                    "available_careers": [
                        recommendation.get("career")
                        for recommendation in recommendations
                    ]
                },
                status=404
            )

        # -----------------------------------------
        # GET MATCHED SKILLS
        # -----------------------------------------

        matched_skills = selected_result.get(
            "matched_skills",
            []
        )

        # -----------------------------------------
        # GET MISSING SKILLS
        # -----------------------------------------

        missing_skills = selected_result.get(
            "missing_skills",
            []
        )

        # -----------------------------------------
        # MAKE SURE THEY ARE LISTS
        # -----------------------------------------

        if not isinstance(
            matched_skills,
            list
        ):

            matched_skills = []

        if not isinstance(
            missing_skills,
            list
        ):

            missing_skills = []

        # -----------------------------------------
        # REQUIRED SKILLS
        # -----------------------------------------

        required_skills = (
            matched_skills +
            missing_skills
        )

        # Remove duplicates
        required_skills = list(
            dict.fromkeys(
                required_skills
            )
        )

        # -----------------------------------------
        # FINAL RESULT
        # -----------------------------------------

        result = {

            "career":
                selected_result.get(
                    "career",
                    career
                ),

            "required_skills":
                required_skills,

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills

        }

        print("-----------------------------------------")
        print("FINAL SKILL GAP RESULT")
        print(result)
        print("-----------------------------------------")

        # -----------------------------------------
        # RETURN RESPONSE
        # -----------------------------------------

        return JsonResponse(
            {
                "success": True,
                "skills": user_skills,
                "career": career,
                "result": result
            }
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "success": False,
                "error": "Invalid JSON request."
            },
            status=400
        )

    except Exception as e:

        print(
            "Skill gap error:",
            str(e)
        )

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

        career = str(
            data.get(
                "career",
                ""
            )
        ).strip()

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

        print(
            "Learning path error:",
            str(e)
        )

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

        print(
            "Multi-hop error:",
            str(e)
        )

        return JsonResponse(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )
