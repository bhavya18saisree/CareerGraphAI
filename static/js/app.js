document.addEventListener("DOMContentLoaded", function () {

    // =========================================================
    // ELEMENTS
    // =========================================================

    const skillElements = document.querySelectorAll(".skill");
    const selectedCount = document.getElementById("selectedCount");

    const analyzeBtn = document.getElementById("analyzeBtn");
    const clearBtn = document.getElementById("clearBtn");

    const loading = document.getElementById("loading");
    const errorBox = document.getElementById("error");

    const results = document.getElementById("results");
    const careerResults = document.getElementById("careerResults");

    const gapSection = document.getElementById("gapSection");
    const gapResults = document.getElementById("gapResults");

    const learningSection =
        document.getElementById("learningSection");

    const learningResults =
        document.getElementById("learningResults");


    // =========================================================
    // CHECK REQUIRED ELEMENTS
    // =========================================================

    if (!skillElements.length) {
        console.error("No .skill elements found.");
    }

    if (!analyzeBtn) {
        console.error("Analyze button not found.");
        return;
    }


    // =========================================================
    // SKILL SELECTION
    // =========================================================

    skillElements.forEach(function (skill) {

        skill.addEventListener("click", function () {

            skill.classList.toggle("selected");

            updateSelectedCount();

            clearError();

        });

    });


    // =========================================================
    // UPDATE SELECTED COUNT
    // =========================================================

    function updateSelectedCount() {

        const count =
            document.querySelectorAll(
                ".skill.selected"
            ).length;

        if (selectedCount) {
            selectedCount.textContent = count;
        }

    }


    // =========================================================
    // GET SELECTED SKILLS
    // =========================================================

    function getSelectedSkills() {

        const selected =
            document.querySelectorAll(
                ".skill.selected"
            );

        return Array.from(selected)
            .map(function (element) {

                return (
                    element.dataset.skill ||
                    element.textContent.trim()
                );

            })
            .filter(function (skill) {

                return skill.trim() !== "";

            });

    }


    // =========================================================
    // ERROR HANDLING
    // =========================================================

    function clearError() {

        if (!errorBox) {
            return;
        }

        errorBox.textContent = "";

        errorBox.style.display = "none";

    }


    function showError(message) {

        if (!errorBox) {
            return;
        }

        errorBox.textContent =
            "❌ " + message;

        errorBox.style.display = "block";

    }


    // =========================================================
    // CLEAR BUTTON
    // =========================================================

    if (clearBtn) {

        clearBtn.addEventListener(
            "click",
            function () {

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
        );

    }


    // =========================================================
    // ANALYZE BUTTON
    // =========================================================

    analyzeBtn.addEventListener(
        "click",
        findCareers
    );


    // =========================================================
    // MAIN CAREER ANALYSIS
    // =========================================================

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

        // No skills selected
        if (selectedSkills.length === 0) {

            showError(
                "Please select at least one skill."
            );

            return;
        }

        // Loading
        if (loading) {
            loading.style.display = "flex";
        }

        analyzeBtn.disabled = true;

        if (results) {
            results.hidden = true;
        }

        try {

            console.log(
                "Selected skills sent to Django:",
                selectedSkills
            );

            // =================================================
            // CALL DJANGO API
            // =================================================

            const response = await fetch(
                "/api/recommend/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"
                    },

                    body: JSON.stringify({
                        skills: selectedSkills
                    })
                }
            );

            console.log(
                "Recommendation API status:",
                response.status
            );

            let data = {};

            try {

                data = await response.json();

            }
            catch (jsonError) {

                throw new Error(
                    "The server returned an invalid response."
                );

            }

            console.log(
                "Recommendation API response:",
                data
            );

            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Unable to generate recommendations."
                );

            }

            let recommendations =
                Array.isArray(
                    data.recommendations
                )
                    ? data.recommendations
                    : [];

            // =================================================
            // FALLBACK
            // =================================================

            if (recommendations.length === 0) {

                console.warn(
                    "Backend returned no recommendations."
                );

                recommendations =
                    generateFallbackRecommendations(
                        selectedSkills
                    );

            }

            if (recommendations.length === 0) {

                throw new Error(
                    "No career recommendations could be generated."
                );

            }

            // =================================================
            // DISPLAY RESULTS
            // =================================================

            displayCareerResults(
                recommendations
            );

            if (results) {

                results.hidden = false;

                setTimeout(
                    function () {

                        results.scrollIntoView({
                            behavior: "smooth",
                            block: "start"
                        });

                    },
                    150
                );

            }

        }
        catch (error) {

            console.error(
                "Recommendation error:",
                error
            );

            showError(
                error.message ||
                "Unable to generate recommendations."
            );

        }
        finally {

            if (loading) {
                loading.style.display = "none";
            }

            analyzeBtn.disabled = false;

        }

    }


    // =========================================================
    // FALLBACK CAREER ENGINE
    // =========================================================

    function generateFallbackRecommendations(
        skills
    ) {

        const normalizedSkills =
            skills.map(function (skill) {

                return skill
                    .toLowerCase()
                    .trim();

            });


        const careerDefinitions = [

            {
                career: "Python Developer",

                skills: [
                    "python",
                    "git",
                    "sql",
                    "rest api",
                    "django"
                ]
            },

            {
                career: "Full Stack Developer",

                skills: [
                    "javascript",
                    "react",
                    "html",
                    "css",
                    "sql",
                    "git",
                    "rest api"
                ]
            },

            {
                career: "Data Analyst",

                skills: [
                    "python",
                    "sql",
                    "statistics",
                    "data analysis"
                ]
            },

            {
                career: "Machine Learning Engineer",

                skills: [
                    "python",
                    "machine learning",
                    "statistics",
                    "data analysis",
                    "sql"
                ]
            },

            {
                career: "Backend Developer",

                skills: [
                    "python",
                    "django",
                    "sql",
                    "rest api",
                    "git"
                ]
            },

            {
                career: "Cloud Engineer",

                skills: [
                    "aws",
                    "docker",
                    "git",
                    "python"
                ]
            },

            {
                career: "DevOps Engineer",

                skills: [
                    "docker",
                    "aws",
                    "git",
                    "python"
                ]
            },

            {
                career: "Frontend Developer",

                skills: [
                    "javascript",
                    "react",
                    "html",
                    "css"
                ]
            },

            {
                career: "Data Scientist",

                skills: [
                    "python",
                    "statistics",
                    "machine learning",
                    "data analysis",
                    "sql"
                ]
            },

            {
                career: "Graph Database Developer",

                skills: [
                    "neo4j",
                    "python",
                    "sql",
                    "rest api"
                ]
            }

        ];


        const results =
            careerDefinitions.map(
                function (career) {

                    const matchedSkills =
                        career.skills.filter(
                            function (required) {

                                return normalizedSkills.includes(
                                    required.toLowerCase()
                                );

                            }
                        );


                    const missingSkills =
                        career.skills.filter(
                            function (required) {

                                return !normalizedSkills.includes(
                                    required.toLowerCase()
                                );

                            }
                        );


                    const score =
                        Math.round(
                            (
                                matchedSkills.length /
                                career.skills.length
                            ) * 100
                        );


                    return {

                        career:
                            career.career,

                        score:
                            score,

                        matched_skills:
                            matchedSkills,

                        missing_skills:
                            missingSkills

                    };

                }
            );


        return results
            .filter(function (result) {

                return result.score > 0;

            })
            .sort(function (a, b) {

                return b.score - a.score;

            })
            .slice(0, 5);

    }


    // =========================================================
    // DISPLAY CAREER RESULTS
    // =========================================================

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

        recommendations
            .slice(0, 5)
            .forEach(
                function (result, index) {

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
                                Number(result.score) || 0
                            )
                        );

                    const missingSkills =
                        Array.isArray(
                            result.missing_skills
                        )
                            ? result.missing_skills
                            : [];

                    const matchedSkills =
                        Array.isArray(
                            result.matched_skills
                        )
                            ? result.matched_skills
                            : [];

                    let missingHTML = "";

                    if (missingSkills.length > 0) {

                        missingHTML = `
                            <span class="missing">
                                ❌ Missing:
                                ${escapeHTML(
                                    missingSkills.join(", ")
                                )}
                            </span>
                        `;

                    }
                    else {

                        missingHTML = `
                            <span class="have">
                                ✅ You have all required skills!
                            </span>
                        `;

                    }

                    let matchedHTML = "";

                    if (matchedSkills.length > 0) {

                        matchedHTML = `
                            <div class="matched-skills">
                                <strong>
                                    Your matching skills:
                                </strong>

                                ${escapeHTML(
                                    matchedSkills.join(", ")
                                )}
                            </div>
                        `;

                    }

                    careerCard.innerHTML = `

                        <h3>
                            🎯
                            ${escapeHTML(
                                result.career ||
                                "Career"
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

                        ${matchedHTML}

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


        // =====================================================
        // SKILL GAP BUTTONS
        // =====================================================

        document
            .querySelectorAll(".gap-button")
            .forEach(
                function (button) {

                    button.addEventListener(
                        "click",
                        function () {

                            showSkillGap(
                                button.dataset.career
                            );

                        }
                    );

                }
            );

    }


    // =========================================================
    // SKILL GAP
    // =========================================================

    async function showSkillGap(career) {

        // IMPORTANT:
        // Get the actual skills selected by the user.
        const selectedSkills =
            getSelectedSkills();

        if (!gapSection || !gapResults) {
            return;
        }

        gapSection.hidden = false;

        gapResults.innerHTML = `

            <div class="gap-box">

                ✨ Loading skill gap...

            </div>

        `;

        gapSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


        try {

            console.log(
                "Skill gap request:",
                {
                    skills: selectedSkills,
                    career: career
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


            console.log(
                "Skill gap response:",
                data
            );


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Unable to load skill gap."
                );

            }


            const result =
                data.result || {};


            // =================================================
            // MATCHED SKILLS
            // =================================================

            const matchedSkills =
                Array.isArray(
                    result.matched_skills
                )
                    ? result.matched_skills
                    : [];


            // =================================================
            // MISSING SKILLS
            // =================================================

            const missingSkills =
                Array.isArray(
                    result.missing_skills
                )
                    ? result.missing_skills
                    : [];


            // =================================================
            // DISPLAY STEP 03
            // =================================================

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
                            selectedSkills.length

                            ? selectedSkills
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
                                    ✓ No skill gap!
                                </div>
                            `
                        }

                    </div>

                </div>

            `;


            // =================================================
            // STEP 04
            // =================================================

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


    // =========================================================
    // LEARNING PATH
    // =========================================================

    async function showLearningPath(career) {

        const selectedSkills =
            getSelectedSkills();


        if (
            !learningSection ||
            !learningResults
        ) {

            return;

        }


        learningSection.hidden = false;


        learningResults.innerHTML = `

            <div class="gap-box">

                ✨ Building your personalized
                learning path...

            </div>

        `;


        try {

            console.log(
                "Learning path request:",
                {
                    skills: selectedSkills,
                    career: career
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


            console.log(
                "Learning path response:",
                data
            );


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


            // =================================================
            // NO MISSING SKILLS
            // =================================================

            if (path.length === 0) {

                learningResults.innerHTML = `

                    <div class="gap-box">

                        🎉 You already have
                        all the required skills!

                    </div>

                `;

                return;

            }


            // =================================================
            // BUILD LEARNING PATH
            // =================================================

            let html = "";


            path.forEach(
                function (item, index) {

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


    // =========================================================
    // HTML ESCAPE
    // =========================================================

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


    // =========================================================
    // INITIAL COUNT
    // =========================================================

    updateSelectedCount();

});