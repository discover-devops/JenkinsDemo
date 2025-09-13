
---

#  **Context – Why This Lab Matters**

CI/CD is no longer just about building code — it’s about **automated deployment**. Most modern apps run in containers (Docker), and production-ready pipelines must:

* Automatically **build container images**
* **Push them to a registry** (like DockerHub)
* And **deploy** them to a server (or Kubernetes)

This lab teaches your students how to go **from source code → Docker image → running container**, all driven by **Jenkins automation**.

 This is **Real CI/CD in Action**, and closely mimics real-world DevOps pipelines in startups and enterprises alike.

---

#  **Concepts – What You’re Teaching**

###  Core Concepts Students Will Learn

| Concept                            | What They’ll Understand                                   |
| ---------------------------------- | --------------------------------------------------------- |
| **Dockerfile**                     | How to containerize any app (Python, Java, Node.js, etc.) |
| **Jenkins Pipeline (Jenkinsfile)** | Code-driven automation of build → push → deploy           |
| **Docker build/push/run**          | The core container lifecycle for dev and prod             |
| **Jenkins with Docker**            | How Jenkins can control Docker CLI directly               |
| **CI/CD Workflow**                 | From Git push to container running on server              |
| **Credential Management**          | Safely connecting to DockerHub or private Git repos       |

---

##  CI/CD Pipeline Flow – Overview Diagram

```text
[GitHub Repo]
     |
     v
[Jenkins]
     |
     ├── Stage 1: Clone source code (Git)
     ├── Stage 2: Build Docker image (docker build)
     ├── Stage 3: Push to DockerHub (docker push)
     └── Stage 4: Deploy to Host (docker run)
     |
     v
[Running Container on Port 5000]
```

This flow gives students a real feel of how companies **deploy services automatically**.

---

#  LAB – Step-by-Step Breakdown

Let’s now structure your **live lab session** so you can teach it smoothly.

---

##  **Step 0: Prep Before Class**

Ensure you have:

* Jenkins running (with Docker CLI access)
* A student-friendly GitHub repo with:

  * `app.py`
  * `requirements.txt`
  * `Dockerfile`
  * `Jenkinsfile`

 Tip: You can clone the repo ahead of time and fork it into your students' GitHub accounts.

---

##  **Step 1: Understanding the App Code**

Explain:

* `app.py` is a simple **Flask** app
* `requirements.txt` lists dependencies
* `Dockerfile` defines the runtime image and startup steps



> “We always containerize our apps using Dockerfile. The final goal of this lab is not just to run the app — but to let **Jenkins** build, push, and deploy it.”

---

##  **Step 2: Docker Setup on Jenkins Host**

Make sure:

```bash
sudo apt update && sudo apt install docker.io -y
sudo usermod -aG docker dockeradmin
sudo systemctl restart docker
```

> Restart Jenkins if `dockeradmin` permissions were just added.

 Run `docker ps` as Jenkins user to confirm Docker access.

---

##  **Step 3: Jenkins Setup**

###  Plugins

Ensure the following Jenkins plugins are installed:

* Docker Pipeline
* Pipeline
* Git
* Publish Over SSH (optional for remote host)

###  Docker Path

Go to:
**Manage Jenkins > Global Tool Configuration > Docker**

* Set Docker installation path (e.g., `/usr/bin/docker`)
* Test Docker from Jenkins terminal

---

##  **Step 4: GitHub Repo Setup**

* Push code (`app.py`, `Dockerfile`, etc.) to your GitHub repo
* Add students as collaborators (or let them fork)
* If private, add credentials to Jenkins

---

##  **Step 5: Jenkinsfile Explained**

Explain **each stage**:

```groovy
pipeline {
  agent any

  environment {
    DOCKER_IMAGE = 'yourrepo/yourapp:latest'
  }

  stages {
    stage('Clone Source Code') {
      steps {
        git branch: 'main', url: 'https://github.com/your-repo.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          docker.build(DOCKER_IMAGE)
        }
      }
    }

    stage('Push Docker Image') {
      steps {
        withDockerRegistry([credentialsId: 'dockerhub-credentials', url: '']) {
          script {
            docker.image(DOCKER_IMAGE).push()
          }
        }
      }
    }

    stage('Deploy Application') {
      steps {
        script {
          sh """
          docker stop my-app || true
          docker rm my-app || true
          docker run -d --name my-app -p 5000:5000 ${DOCKER_IMAGE}
          """
        }
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}
```

 

> “This file is our **pipeline blueprint**. Jenkins reads this and runs every stage one after another, like a build robot.”

---

##  **Step 6: Run the Jenkins Job**

1. **Create a new Jenkins Pipeline job**
2. Choose **Pipeline from SCM**
3. Paste your GitHub repo URL
4. Set branch = `main`
5. Jenkinsfile = `Jenkinsfile`

 Click **Build Now**

Watch the console:

* Cloning code
* Building Docker image
* Pushing to DockerHub
* Running container

---

##  **Step 7: Access the App**

Visit:

```
http://<jenkins-host>:5000
```

You’ll see:

```
Hello, World! This is my Jenkins CI/CD pipeline demo.
```

 Success! Full CI/CD pipeline with container deployment complete!

---

##  **Step 8: Optional GitHub Webhook (Auto-Trigger)**

Teach students how to:

1. Add GitHub webhook:

   * URL: `http://<jenkins-host>:8080/github-webhook/`
2. Push new code
3. Jenkins auto-triggers pipeline!

---

##  Step 9: Troubleshooting & FAQs

| Issue                             | Fix                                         |
| --------------------------------- | ------------------------------------------- |
| `docker: permission denied`       | Jenkins user not in Docker group            |
| `Cannot connect to Docker daemon` | Docker not running or incorrect socket      |
| Pipeline not triggering           | Check webhook, or click “Build Now”         |
| Image not pushed                  | Check DockerHub credentials and permissions |

---

##  Summary Slide for Students

| What You Learned | Description                           |
| ---------------- | ------------------------------------- |
| Dockerfile       | Containerizing the Python app         |
| Jenkinsfile      | Automating build → push → deploy      |
| Jenkins Pipeline | Managing CI/CD stages                 |
| Docker Commands  | Building, pushing, running containers |
| Webhooks         | Auto-triggered CI/CD pipelines        |

---

