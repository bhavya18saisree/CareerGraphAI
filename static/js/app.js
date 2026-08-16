/* =========================================================
   CAREERGRAPH AI - COMPLETE FRONTEND JAVASCRIPT
========================================================= */

"use strict";

/* =========================================================
   DOM ELEMENTS
========================================================= */

const skillElements = document.querySelectorAll(".skill");

const selectedCount =
    document.getElementById("selectedCount");

const analyzeBtn =
    document.getElementById("analyzeBtn");

const clearBtn =
    document.getElementById("clearBtn");

const loading =
    document.getElementById("loading");

const errorBox =
    document.getElementById("error");

const results =
    document.getElementById("results");

const careerResults =
    document.getElementById("careerResults");

const gapSection =
    document.getElementById("gapSection");

const gapResults =
    document.getElementById("gapResults");

const learningSection =
    document.getElementById("learningSection");

const learningResults =
    document.getElementById("learningResults");


/* =========================================================
   INITIALIZATION
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    updateSelectedCount();

    /* -----------------------------------------
       SKILL BUTTONS
    ----------------------------------------- */

    skillElements.forEach(function (skill) {

        skill.addEventListener("click", function () {

            skill.classList.toggle("selected");

            updateSelectedCount();

            clearError();

        });

    });


    /* -----------------------------------------
       ANALYZE BUTTON
    ----------------------------------------- */

    if (analyzeBtn) {

        analyzeBtn.addEventListener(
            "click",
            findCareers
        );

    }


    /* -----------------------------------------
       CLEAR BUTTON
    ----------------------------------------- */

    if (clearBtn) {

        clearBtn.addEventListener(
            "click",
            clearAll
        );

    }

});


/* =========================================================
   UPDATE SELECTED SKILL COUNT
========================================================= */

function updateSelectedCount() {

    const count =
        document.querySelectorAll(
            ".skill.selected"
        ).length;

    if (selectedCount) {

        selectedCount.textContent = count;

    }

}


/* =========================================================
   GET SELECTED SKILLS
========================================================= */

function getSelectedSkills() {

    const selected =
        document.querySelectorAll(
            ".skill.selected"
        );

    return Array.from(selected).map(
        function (element) {

            return element.dataset.skill;

        }
    );

}


/* =========================================================
   CLEAR EVERYTHING
========================================================= */

function clearAll() {

    skillElements.forEach(
        function (skill) {

            skill.classList.remove(
                "selected"
            );

        }
    );

    updateSelectedCount();

    clearError();


    if (results) {

        results.hidden = true;

    }


    if (gapSection) {

        gapSection.hidden = true;

    }


    if (learningSection) {

        learningSection.hidden = true;

    }


    if (careerResults) {

        careerResults.innerHTML = "";

    }


    if (gapResults) {

        gapResults.innerHTML = "";

    }


    if (learningResults) {

        learningResults.innerHTML = "";

    }

}


/* =========================================================
   CLEAR ERROR
========================================================= */

function clearError() {

    if (!errorBox) {

        return;

    }

    errorBox.textContent = "";

    errorBox.style.display = "none";

}


/* =========================================================
   SHOW ERROR
========================================================= */

function showError(message) {

    if (!errorBox) {

        alert(message);

        return;

    }

    errorBox.textContent =
        "❌ " + message;

    errorBox.style.display =
        "block";

}


/* =========================================================
   ANALYZE CAREER
========================================================= */

async function findCareers() {

    const selectedSkills =
        getSelectedSkills();


    clearError();


    if (gapSection) {

        gapSection.hidden = true;

    }


    if (learningSection) {

        learningSection.hidden = true;

    }


    /* -----------------------------------------
       CHECK SKILLS
    ----------------------------------------- */

    if (selectedSkills.length === 0) {

        showError(
            "Please select at least one skill."
        );

        return;

    }


    /* -----------------------------------------
       LOADING
    ----------------------------------------- */

    if (loading) {

        loading.style.display = "flex";

    }


    if (analyzeBtn) {

        analyzeBtn.disabled = true;

    }


    if (results) {

        results.hidden = true;

    }


    try {

        console.log(
            "Selected skills:",
            selectedSkills
        );


        /* -----------------------------------------
           API REQUEST
        ----------------------------------------- */

        const response =
            await fetch(
                "/api/recommend/",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            skills:
                                selectedSkills

                        })

                }
            );


        console.log(
            "Recommendation API status:",
            response.status
        );


        /* -----------------------------------------
           READ RESPONSE
        ----------------------------------------- */

        const responseText =
            await response.text();


        console.log(
            "Recommendation API response:",
            responseText
        );


        let data;


        try {

            data =
                JSON.parse(
                    responseText
                );

        }
        catch (jsonError) {

            throw new Error(
                "Server returned an invalid response. HTTP status: " +
                response.status
            );

        }


        /* -----------------------------------------
           API ERROR
        ----------------------------------------- */

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to generate career recommendations."
            );

        }


        /* -----------------------------------------
           CHECK RESPONSE
        ----------------------------------------- */

        if (
            !data ||
            !Array.isArray(
                data.recommendations
            )
        ) {

            throw new Error(
                "The server did not return valid career recommendations."
            );

        }


        if (
            data.recommendations.length === 0
        ) {

            throw new Error(
                "No career recommendations were found for the selected skills."
            );

        }


        /* -----------------------------------------
           DISPLAY RESULTS
        ----------------------------------------- */

        displayCareerResults(
            data.recommendations
        );


        if (results) {

            results.hidden = false;

        }


        /* -----------------------------------------
           SCROLL TO RESULTS
        ----------------------------------------- */

        setTimeout(
            function () {

                if (results) {

                    results.scrollIntoView({

                        behavior:
                            "smooth",

                        block:
                            "start"

                    });

                }

            },
            100
        );

    }
    catch (error) {

        console.error(
            "Career recommendation error:",
            error
        );


        showError(
            error.message ||
            "Something went wrong while analyzing your career."
        );

    }
    finally {

        if (loading) {

            loading.style.display =
                "none";

        }


        if (analyzeBtn) {

            analyzeBtn.disabled =
                false;

        }

    }

}


/* =========================================================
   DISPLAY CAREER RESULTS
========================================================= */

function displayCareerResults(
    recommendations
) {

    if (!careerResults) {

        console.error(
            "careerResults element not found."
        );

        return;

    }


    careerResults.innerHTML = "";


    /* -----------------------------------------
       LIMIT TO TOP 5
    ----------------------------------------- */

    const topResults =
        recommendations.slice(
            0,
            5
        );


    topResults.forEach(
        function (result, index) {

            const careerCard =
                document.createElement(
                    "div"
                );


            careerCard.className =
                "career";


            careerCard.style.animationDelay =
                `${index * 0.1}s`;


            /* -----------------------------------------
               CAREER NAME
            ----------------------------------------- */

            const careerName =
                result.career ||
                result.title ||
                "Career";


            /* -----------------------------------------
               SCORE
            ----------------------------------------- */

            let score =
                Number(
                    result.score
                );


            if (Number.isNaN(score)) {

                score = 0;

            }


            score =
                Math.max(
                    0,
                    Math.min(
                        100,
                        score
                    )
                );


            /* -----------------------------------------
               MISSING SKILLS
            ----------------------------------------- */

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

                missingHTML = `

                    <div class="missing-skills">

                        ❌ Missing:

                        ${escapeHTML(
                            missingSkills.join(", ")
                        )}

                    </div>

                `;

            }
            else {

                missingHTML = `

                    <span class="have">

                        ✅ You have all
                        required skills!

                    </span>

                `;

            }


            /* -----------------------------------------
               CAREER CARD HTML
            ----------------------------------------- */

            careerCard.innerHTML = `

                <h3>

                    🎯

                    ${escapeHTML(
                        careerName
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
                        careerName
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


    /* -----------------------------------------
       SKILL GAP BUTTONS
    ----------------------------------------- */

    document
        .querySelectorAll(
            ".gap-button"
        )
        .forEach(
            function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        const career =
                            button.dataset.career;

                        showSkillGap(
                            career
                        );

                    }
                );

            }
        );

}


/* =========================================================
   SHOW SKILL GAP
========================================================= */

async function showSkillGap(
    career
) {

    const selectedSkills =
        getSelectedSkills();


    if (!career) {

        showError(
            "Career information is missing."
        );

        return;

    }


    if (gapSection) {

        gapSection.hidden = false;

    }


    if (gapResults) {

        gapResults.innerHTML = `

            <div class="gap-box">

                ✨ Loading skill gap...

            </div>

        `;

    }


    if (gapSection) {

        gapSection.scrollIntoView({

            behavior:
                "smooth",

            block:
                "start"

        });

    }


    try {

        console.log(
            "Skill gap request:",
            {
                skills:
                    selectedSkills,

                career:
                    career
            }
        );


        const response =
            await fetch(
                "/api/skill-gap/",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            skills:
                                selectedSkills,

                            career:
                                career

                        })

                }
            );


        const responseText =
            await response.text();


        let data;


        try {

            data =
                JSON.parse(
                    responseText
                );

        }
        catch (error) {

            throw new Error(
                "Skill-gap API returned an invalid response."
            );

        }


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to load skill gap."
            );

        }


        if (!data.result) {

            throw new Error(
                "Skill-gap information was not returned."
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


        /* -----------------------------------------
           DISPLAY SKILL GAP
        ----------------------------------------- */

        if (gapResults) {

            gapResults.innerHTML = `

                <div class="gap-box">

                    <h3>

                        🎯

                        ${escapeHTML(
                            result.career ||
                            career
                        )}

                    </h3>


                    <div class="skill-list">

                        <strong>
                            Your Skills
                        </strong>


                        ${
                            matchedSkills.length > 0

                                ? matchedSkills
                                    .map(
                                        function (skill) {

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

                                : `

                                    <div>
                                        No matching skills found.
                                    </div>

                                `
                        }


                        <br>


                        <strong>
                            Skills You Need
                        </strong>


                        ${
                            missingSkills.length > 0

                                ? missingSkills
                                    .map(
                                        function (skill) {

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

                                        ✓
                                        No skill gap!

                                    </div>

                                `
                        }

                    </div>

                </div>

            `;

        }


        /* -----------------------------------------
           LOAD LEARNING PATH
        ----------------------------------------- */

        await showLearningPath(
            career
        );

    }
    catch (error) {

        console.error(
            "Skill gap error:",
            error
        );


        if (gapResults) {

            gapResults.innerHTML = `

                <div class="gap-box">

                    <div
                        class="error"
                        style="display:block"
                    >

                        ❌

                        ${escapeHTML(
                            error.message
                        )}

                    </div>

                </div>

            `;

        }

    }

}


/* =========================================================
   SHOW LEARNING PATH
========================================================= */

async function showLearningPath(
    career
) {

    const selectedSkills =
        getSelectedSkills();


    if (learningSection) {

        learningSection.hidden =
            false;

    }


    if (learningResults) {

        learningResults.innerHTML = `

            <div class="gap-box">

                ✨ Building your personalized
                learning path...

            </div>

        `;

    }


    try {

        console.log(
            "Learning path request:",
            {
                skills:
                    selectedSkills,

                career:
                    career

            }
        );


        const response =
            await fetch(
                "/api/learning-path/",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            skills:
                                selectedSkills,

                            career:
                                career

                        })

                }
            );


        const responseText =
            await response.text();


        let data;


        try {

            data =
                JSON.parse(
                    responseText
                );

        }
        catch (error) {

            throw new Error(
                "Learning-path API returned an invalid response."
            );

        }


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


        /* -----------------------------------------
           NO LEARNING REQUIRED
        ----------------------------------------- */

        if (path.length === 0) {

            if (learningResults) {

                learningResults.innerHTML = `

                    <div class="gap-box">

                        🎉 You already have
                        all the required skills!

                    </div>

                `;

            }

            return;

        }


        /* -----------------------------------------
           BUILD LEARNING PATH
        ----------------------------------------- */

        let html = "";


        path.forEach(
            function (item, index) {

                const skill =
                    item.skill ||
                    "Skill";


                const courses =
                    Array.isArray(
                        item.courses
                    )
                        ? item.courses
                        : [];


                html += `

                    <div class="gap-box">

                        <div class="path-title">

                            ${index + 1}.

                            📌 Missing Skill:

                            ${escapeHTML(
                                skill
                            )}

                        </div>

                `;


                if (
                    courses.length > 0
                ) {

                    courses.forEach(
                        function (course) {

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


        if (learningResults) {

            learningResults.innerHTML =
                html;

        }

    }
    catch (error) {

        console.error(
            "Learning path error:",
            error
        );


        if (learningResults) {

            learningResults.innerHTML = `

                <div class="gap-box">

                    <div
                        class="error"
                        style="display:block"
                    >

                        ❌

                        ${escapeHTML(
                            error.message
                        )}

                    </div>

                </div>

            `;

        }

    }

}


/* =========================================================
   OPTIONAL MULTI-HOP ANALYSIS
========================================================= */

async function getMultiHopRecommendations() {

    const selectedSkills =
        getSelectedSkills();


    if (selectedSkills.length === 0) {

        showError(
            "Please select at least one skill."
        );

        return;

    }


    try {

        const response =
            await fetch(
                "/api/multi-hop/",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            skills:
                                selectedSkills

                        })

                }
            );


        const responseText =
            await response.text();


        let data;


        try {

            data =
                JSON.parse(
                    responseText
                );

        }
        catch (error) {

            throw new Error(
                "Multi-hop API returned an invalid response."
            );

        }


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to load multi-hop recommendations."
            );

        }


        console.log(
            "Multi-hop recommendations:",
            data.multi_hop_results
        );


        return data.multi_hop_results;

    }
    catch (error) {

        console.error(
            "Multi-hop error:",
            error
        );


        showError(
            error.message
        );

        return [];

    }

}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escapeHTML(value) {

    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}


/* =========================================================
   INITIAL COUNT
========================================================= */

updateSelectedCount();