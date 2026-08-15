from django.urls import path
from .views import (career_recommendation, skill_gap,learning_path,multi_hop)
urlpatterns = [
    path("recommend/",career_recommendation,name="career_recommendation"),
    path("skill-gap/",skill_gap,name="skill_gap" ),
    path("learning-path/",learning_path,name="learning_path"),
    path("multi-hop/", multi_hop, name="multi_hop"),
]