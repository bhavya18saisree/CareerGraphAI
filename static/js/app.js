const skillElements =document.querySelectorAll(".skill");
const selectedCount = document.getElementById("selectedCount");
const analyzeBtn =document.getElementById("analyzeBtn");
const clearBtn =document.getElementById("clearBtn");
const loading =document.getElementById("loading");
const errorBox =document.getElementById("error");
const results =document.getElementById("results");
const careerResults =document.getElementById("careerResults");
const gapSection =document.getElementById("gapSection");
const gapResults =document.getElementById("gapResults");
const learningSection =document.getElementById("learningSection");
const learningResults =document.getElementById("learningResults");
skillElements.forEach(function(skill) {
    skill.addEventListener("click", function() {
        skill.classList.toggle("selected");
        updateSelectedCount();
        clearError();
    });
});
function updateSelectedCount() {
 const count =document.querySelectorAll(".skill.selected" ).length;
    selectedCount.textContent = count;
}
function getSelectedSkills() {

    const selected =
        document.querySelectorAll(
            ".skill.selected"
        );

    return Array.from(selected).map(
        function(element) {

            return element.dataset.skill;

        }
    );

}


/* =========================================
   CLEAR ERROR
========================================= */

function clearError() {

    errorBox.textContent = "";

    errorBox.style.display = "none";

}


/* =========================================
   SHOW ERROR
========================================= */

function showError(message) {

    errorBox.textContent =
        "❌ " + message;

    errorBox.style.display =
        "block";

}
clearBtn.addEventListener(
    "click",
    function() {
        skillElements.forEach(
            function(skill) {
                skill.classList.remove(
                    "selected"
                ); } );
        updateSelectedCount();
        clearError();
        results.hidden = true;
        gapSection.hidden = true;
        learningSection.hidden = true;
        careerResults.innerHTML = "";
        gapResults.innerHTML = "";
        learningResults.innerHTML = "";

    }
);
analyzeBtn.addEventListener("click",findCareers);
async function findCareers() {

    const selectedSkills =getSelectedSkills();
    clearError();
    gapSection.hidden = true;
    learningSection.hidden = true;
    if (selectedSkills.length === 0) {
        showError(
            "Please select at least one skill."
        );

        return;

    }


    loading.style.display =
        "flex";


    analyzeBtn.disabled =
        true;


    results.hidden =
        true;


    try {


        const response =
            await fetch(
                "/api/recommend/",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        skills:
                            selectedSkills

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to generate recommendations."
            );

        }


        displayCareerResults(
            data.recommendations
        );


        results.hidden =
            false;


        setTimeout(
            function() {

                results.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            },
            100
        );


    }
    catch (error) {

        console.error(
            "Recommendation error:",
            error
        );


        showError(
            error.message
        );

    }
    finally {

        loading.style.display =
            "none";

        analyzeBtn.disabled =
            false;

    }

}
function displayCareerResults(
    recommendations
) {

    careerResults.innerHTML = "";
    recommendations
        .slice(0, 5)
        .forEach(
            function(result, index) {

                const careerCard =
                    document.createElement(
                        "div"
                    );


                careerCard.className =
                    "career";


                careerCard.style.animationDelay =
                    `${index * 0.1}s`;


                const score =
                    Math.max(
                        0,
                        Math.min(
                            100,
                            Number(result.score)
                        )
                    );


                const missingSkills =
                    Array.isArray(
                        result.missing_skills
                    )
                    ? result.missing_skills
                    : [];


                let missingHTML;


                if (
                    missingSkills.length > 0
                ) {

                    missingHTML =
                        `
                        ❌ Missing:
                        ${escapeHTML(
                            missingSkills.join(", ")
                        )}
                        `;

                }
                else {

                    missingHTML =
                        `
                        <span
                            class="have"
                        >
                            ✅ You have all
                            required skills!
                        </span>
                        `;

                }


                careerCard.innerHTML = `

                    <h3>
                        🎯
                        ${escapeHTML(
                            result.career
                        )}
                    </h3>


                    <div class="score-row">

                        <span>
                            Career Match
                        </span>

                        <span class="score">
                            ${score}%
                        </span>

                    </div>


                    <div class="progress">

                        <div
                            class="progress-bar"
                            style="width: ${score}%"
                        ></div>

                    </div>


                    <p class="missing">

                        ${missingHTML}

                    </p>


                    <button
                        type="button"
                        class="gap-button"
                        data-career="${escapeHTML(
                            result.career
                        )}"
                    >

                        🎯 View Skill Gap

                    </button>

                `;


                careerResults.appendChild(
                    careerCard
                );

            }
        );


    document
        .querySelectorAll(".gap-button")
        .forEach(
            function(button) {

                button.addEventListener(
                    "click",
                    function() {

                        showSkillGap(
                            button.dataset.career
                        );

                    }
                );

            }
        );

}
async function showSkillGap(
    career
) {

    const selectedSkills =
        getSelectedSkills();


    gapSection.hidden =
        false;


    gapResults.innerHTML =
        `

        <div class="gap-box">

            ✨ Loading skill gap...

        </div>

        `;


    gapSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
    try {
        const response =
            await fetch(
                "/api/skill-gap/",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        skills:
                            selectedSkills,

                        career:
                            career

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to load skill gap."
            );

        }


        const result =
            data.result;


        const matchedSkills =
            Array.isArray(
                result.matched_skills
            )
            ? result.matched_skills
            : [];


        const missingSkills =
            Array.isArray(
                result.missing_skills
            )
            ? result.missing_skills
            : [];


        gapResults.innerHTML = `

            <div class="gap-box">

                <h3>
                    🎯
                    ${escapeHTML(
                        result.career
                    )}
                </h3>


                <div class="skill-list">

                    <strong>
                        Your Skills
                    </strong>


                    ${
                        matchedSkills.length

                        ? matchedSkills
                            .map(
                                function(skill) {

                                    return `
                                        <div class="have">
                                            ✓
                                            ${escapeHTML(
                                                skill
                                            )}
                                        </div>
                                    `;

                                }
                            )
                            .join("")

                        : "<div>None</div>"
                    }


                    <br>


                    <strong>
                        Skills You Need
                    </strong>


                    ${
                        missingSkills.length

                        ? missingSkills
                            .map(
                                function(skill) {

                                    return `
                                        <div class="need">
                                            ✗
                                            ${escapeHTML(
                                                skill
                                            )}
                                        </div>
                                    `;

                                }
                            )
                            .join("")

                        : `
                            <div class="have">
                                ✓ No skill gap!
                            </div>
                        `
                    }

                </div>

            </div>

        `;


        await showLearningPath(
            career
        );

    }
    catch (error) {

        console.error(
            "Skill gap error:",
            error
        );


        gapResults.innerHTML = `

            <div class="gap-box">

                <div class="error"
                     style="display:block">

                    ❌
                    ${escapeHTML(
                        error.message
                    )}

                </div>

            </div>

        `;

    }

}


/* =========================================
   LEARNING PATH
========================================= */

async function showLearningPath(
    career
) {

    const selectedSkills =
        getSelectedSkills();


    learningSection.hidden =
        false;


    learningResults.innerHTML =
        `

        <div class="gap-box">

            ✨ Building your personalized
            learning path...

        </div>

        `;


    try {


        const response =
            await fetch(
                "/api/learning-path/",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        skills:
                            selectedSkills,

                        career:
                            career

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to load learning path."
            );

        }


        const path =
            Array.isArray(
                data.learning_path
            )
            ? data.learning_path
            : [];


        if (path.length === 0) {

            learningResults.innerHTML = `

                <div class="gap-box">

                    🎉 You already have
                    all the required skills!

                </div>

            `;

            return;

        }


        let html = "";


        path.forEach(
            function(item, index) {

                html += `

                    <div class="gap-box">

                        <div class="path-title">

                            ${index + 1}.
                            📌 Missing Skill:
                            ${escapeHTML(
                                item.skill
                            )}

                        </div>

                `;


                const courses =
                    Array.isArray(
                        item.courses
                    )
                    ? item.courses
                    : [];


                if (courses.length > 0) {

                    courses.forEach(
                        function(course) {

                            html += `

                                <div class="course">

                                    📚
                                    ${escapeHTML(
                                        course
                                    )}

                                </div>

                            `;

                        }
                    );

                }
                else {

                    html += `

                        <div class="course">

                            No course currently
                            available.

                        </div>

                    `;

                }


                html += `

                    </div>

                `;

            }
        );


        learningResults.innerHTML =
            html;

    }
    catch (error) {

        console.error(
            "Learning path error:",
            error
        );


        learningResults.innerHTML = `

            <div class="gap-box">

                <div class="error"
                     style="display:block">

                    ❌
                    ${escapeHTML(
                        error.message
                    )}

                </div>

            </div>

        `;

    }

}


function escapeHTML(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace( /</g,"&lt;")
        .replace(/>/g,"&gt;")
        .replace( /"/g, "&quot;")
        .replace(/'/g,"&#039;"
        );
}
updateSelectedCount();