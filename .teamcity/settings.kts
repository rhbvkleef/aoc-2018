import jetbrains.buildServer.configs.kotlin.v2018_2.*
import jetbrains.buildServer.configs.kotlin.v2018_2.buildFeatures.commitStatusPublisher
import jetbrains.buildServer.configs.kotlin.v2018_2.buildSteps.script
import jetbrains.buildServer.configs.kotlin.v2018_2.triggers.vcs

/*
The settings script is an entry point for defining a TeamCity
project hierarchy. The script should contain a single call to the
project() function with a Project instance or an init function as
an argument.

VcsRoots, BuildTypes, Templates, and subprojects can be
registered inside the project using the vcsRoot(), buildType(),
template(), and subProject() methods respectively.

To debug settings scripts in command-line, run the

    mvnDebug org.jetbrains.teamcity:teamcity-configs-maven-plugin:generate

command and attach your debugger to the port 8000.

To debug in IntelliJ Idea, open the 'Maven Projects' tool window (View
-> Tool Windows -> Maven Projects), find the generate task node
(Plugins -> teamcity-configs -> teamcity-configs:generate), the
'Debug' option is available in the context menu for the task.
*/

version = "2018.2"

project {

    buildType(Build)

    params {
        password("aoc_auth_token", "credentialsJSON:40ffef22-0d0b-41f9-8170-50ae87183e15", label = "aoc_auth_token", description = "Advent of Code session token", display = ParameterDisplay.HIDDEN)
    }

    features {
        feature {
            id = "PROJECT_EXT_6"
            type = "IssueTracker"
            param("secure:password", "")
            param("name", "rhbvkleef/aoc-2018")
            param("pattern", """#(\d+)""")
            param("authType", "accesstoken")
            param("repository", "https://github.com/rhbvkleef/aoc-2018")
            param("type", "GithubIssues")
            param("secure:accessToken", "credentialsJSON:908ed917-04bb-4d48-9e4c-8a8c97a41e77")
            param("username", "")
        }
    }
}

object Build : BuildType({
    name = "Test"

    artifactRules = """
        htmlcov => htmlcov
        results => results
        answers.json => results
    """.trimIndent()

    vcs {
        root(DslContext.settingsRoot)
    }

    steps {
        script {
            name = "Setup"
            scriptContent = """
                pipenv --python 3.6
                pipenv install --dev
                pipenv run pip freeze
                
                echo "URL = \"https://adventofcode.com/2018/day/{}/input\"\nSESSION = \"%aoc_auth_token%\"" > config.py
            """.trimIndent()
        }
        script {
            name = "Test"
            scriptContent = """
                export TEAMCITY='enabled'
                
                pipenv run coverage run manage.py test all
            """.trimIndent()
        }
        script {
            name = "Run"
            scriptContent = "pipenv run python manage.py run all"
        }
        script {
            name = "Report"
            scriptContent = """
                rm -rf htmlcov
                
                pipenv run coverage html
                pipenv run coverage-badge -o htmlcov/coverage.svg
                
                COVERAGE=${'$'}(cat ./htmlcov/index.html | grep '<span class="pc_cov">' | grep -o '[0-9]\+');
                
                echo "##teamcity[buildStatisticValue key='CodeCoverageL' value='${'$'}COVERAGE']"
            """.trimIndent()
        }
    }

    triggers {
        vcs {
        }
    }

    features {
        commitStatusPublisher {
            vcsRootExtId = "${DslContext.settingsRoot.id}"
            publisher = github {
                githubUrl = "https://api.github.com"
                authType = personalToken {
                    token = "credentialsJSON:333fa003-05a8-472a-9f85-7d3b8cdb5e5f"
                }
            }
            param("github_oauth_user", "rhbvkleef")
        }
    }
})
