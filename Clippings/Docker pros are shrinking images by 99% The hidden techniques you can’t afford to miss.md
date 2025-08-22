---
title: "Docker pros are shrinking images by 99%: The hidden techniques you can’t afford to miss"
source: "https://aws.plainenglish.io/docker-pros-are-shrinking-images-by-99-the-hidden-techniques-you-cant-afford-to-miss-a70ee26b4cbf"
author:
  - "[[Dipanshu ‎]]"
published: 2024-09-18
created: 2025-02-17
description: "Unlock the secret to slashing Docker image sizes by 99%. Discover expert strategies for faster, lightweight containers that boost performance and efficiency."
tags:
  - "clippings"
---
## Unlock the secrets to lightning-fast deployments and slashed costs — before your competitors do

[

![Dipanshu ‎](https://miro.medium.com/v2/resize:fill:88:88/1*SToMouWcalbMTg3N3mERqQ.png)

](https://dipanshu10.medium.com/?source=post_page---byline--a70ee26b4cbf---------------------------------------)

[

![AWS in Plain English](https://miro.medium.com/v2/resize:fill:48:48/1*6EeD87OMwKk-u3ncwAOhog.png)

](https://aws.plainenglish.io/?source=post_page---byline--a70ee26b4cbf---------------------------------------)

![](https://miro.medium.com/v2/resize:fit:1400/1*nMPH6k5nc-LzH6oNd5kB4g.png)

Image by author

> ==[Non-Medium Members Can Read the Full Article by Clicking Here.](https://medium.com/aws-in-plain-english/docker-pros-are-shrinking-images-by-99-the-hidden-techniques-you-cant-afford-to-miss-a70ee26b4cbf?sk=e900c270625854bf314e7dcd7b6523ad)==

Are you tired of wrestling with bloated Docker images that eat up your disk space and slow down your deployments? You’re not alone. But here’s the kicker: **top DevOps teams are already slashing their image sizes by up to 99%**. In this guide, i’ll unveil the techniques they’ve been keeping under wraps.

## The Hidden Cost of Bloated Docker Images

Before we dive into the solutions, let’s talk about why this matters. Oversized Docker images aren’t just a nuisance — they’re costing you:

**Time**: Slower build and deployment cycles

**Money**: Increased storage and bandwidth costs

**Performance**: Reduced application responsiveness

## The Journey from 1.2GB to 8MB: A Case Study

To illustrate the power of these techniques, let’s look at a real-world example. we took a standard Python-based machine learning application with an initial Docker image size of 1.2GB and optimized it down to a mere 8MB. Here’s how we did it:

1. Multi-stage builds
2. Layer optimizations
3. Minimal base images (including Scratch)
4. Advanced techniques like distroless images
5. Security best practices

## Starting point: the bloated image

this is usually a typical Dockerfile you might encounter

```
FROM python:3.9WORKDIR /appCOPY requirements.txt .RUN pip install -r requirements.txtCOPY . .CMD ["python", "main.py"]
```

This Dockerfile, while functional, results in a large image size due to:

1. Using a full Python image
2. Including unnecessary build tools and dependencies
3. Inefficient layer caching
4. Potential inclusion of unnecessary files

Now lets look into the techniques that will help you optimize image

## Multi-Stage Builds : The Game-Changer

Multi-stage builds are a powerful technique to dramatically reduce your final Docker image size.It allows us to separate build-time dependencies from runtime ones.

- **Use a minimal Base Image**

replace the full python version with a slim or alpine version according to your use case

```
FROM python:3.9-slim AS builder
```

## Single-Stage Dockerfile

```
FROM python:3.9-slim
```
```
# Install necessary build dependenciesRUN apt-get update && apt-get install -y --no-install-recommends \    build-essential \    gcc \    && rm -rf /var/lib/apt/lists/*# Set the working directoryWORKDIR /app# Copy the requirements file and install dependenciesCOPY requirements.txt ./RUN pip install --no-cache-dir -r requirements.txt# Copy the rest of the application codeCOPY . .# Compile the model (if necessary)RUN python compile_model.py# Run the inference scriptCMD ["python", "inference.py"]
```

Building this image results in approximately 1.2GB. this large size is due to inclusion of all the build tools and development libraries.

## Multi-Stage Dockerfile

**Stage 1: Build Stage**

- we will setup working directory
- Install necessary build tools
- Copy and Install our python dependencies
- Copy Application code
- Use PyInstaller to Create a standalone executable

```
FROM python:3.9-slim AS builder
```
```
# Install necessary build dependenciesRUN apt-get update && apt-get install -y --no-install-recommends \    build-essential \    gcc \    && rm -rf /var/lib/apt/lists/*# Set the working directoryWORKDIR /app# Copy the requirements file and install dependenciesCOPY requirements.txt ./RUN pip install --no-cache-dir -r requirements.txt# Copy the application codeCOPY . .# Compile the model (if necessary)RUN python compile_model.py# Install PyInstallerRUN pip install pyinstaller# Create a standalone executableRUN pyinstaller --onefile inference.py
```

**Stage 2: Production Stage**

- start from a `scratch` image - a totally empty image
- copy only the necessary files from `Build stage`
- We set the entry-point to compiled application

```
FROM scratch
```
```
# Set the working directoryWORKDIR /app# Copy only the necessary files from the build stageCOPY --from=builder /app/dist/inference /app/inferenceCOPY --from=builder /app/model /app/model# Run the inference executableENTRYPOINT ["/app/inference"]
```

Building this multi-stage Dockerfile results in an image size of approximately **85 MB** — a reduction of over **90%**

## Layer Optimization: Every Byte Counts

Each instruction you write in you Dockerfile Creates a new layer in Docker image.For example RUN,COPY and ADD commands each add a layer and each layer adds image size as well as the built time

- **Minimize Layers**: Combining multiple run commands into single RUN instruction this approach minimizes redundant layers and keeps the image cleaner.For example: instead of Separate RUN commands for installing packages and cleaning up temporary files, you should combine them.
- Use **&&** to chain commands and clean up in the same layer.

```
RUN apt-get update && apt-get install -y python3-pip python3-dev && \    pip3 install numpy pandas && \    apt-get clean && rm -rf /var/lib/apt/lists/*
```

## Minimal Base Images from Scratch : Less is More

This is the most powerful,but also most challenging way to create a Docker Image.Creating an image from scratch means that you use the [scratch base image](https://hub.docker.com/_/scratch). No underlying operating system. No dependencies. No preexisting data or applications. Think of it like an empty storage disc, you have to populate it with data because there is nothing in it.

whatever you put in it will contribute to its size.But this does mean that if you need any dependencies or supporting applications or tools, you will need to install them on the image, your self.

it can be **useful in two scenarios** mainly:

- when you are **creating your own base image**.For example. You created your own Linux distribution, right. You don’t want to put this on top of another base image, like ubuntu or something. You can use a scratch image instead, and then put your own Linux distribution on top of it.
- When you have a **standalone executable application**.For example for a standalone Python-based ML/DL application, such as a model server handling predictions, you can compile the code into an executable using tools like PyInstaller . Once compiled, place the executable in a scratch Docker image. Since this image lacks an OS or libraries, you’ll need to manually add only the necessary dependencies (e.g., TensorFlow, PyTorch, model files, or config files). This keeps the image minimal and optimized for deployment.

```
# syntax=docker/dockerfile:1FROM scratchADD myapp /CMD ["/myapp"]
```

## Advanced Techniques:

## Distroless Images

Imagine you’re packing for a trip. You have three options:

1. Pack your entire wardrobe (Full Distribution Image)
2. Pack nothing and buy everything at your destination (Scratch Image)
3. Pack only what you’ll actually need (Distroless Image)

[**Google’s distroless images**](https://github.com/GoogleContainerTools/distroless) provide a middle ground between full distributions and scratch images. This is the “just right” option. It includes only what’s necessary to run your application.

Distroless images are special because they:

- Are smaller than full distribution images
- Are **more secure** because they have fewer unnecessary components
- Still include important things like SSL certificates and timezone data

```
FROM gcr.io/distroless/python3-debian10COPY --from=builder /app/dist/main /app/mainCOPY --from=builder /app/model /app/modelCOPY --from=builder /app/config.yml /app/config.ymlENTRYPOINT ["/app/main"]
```

## Use Docker Buildkit

Docker BuildKit offers improved performance, security and more flexible cache invalidation for building docker images. Enable it with

```
DOCKER_BUILDKIT=1 docker build -t myapp .
```

## Other techniques :

- **Eliminating Unnecesary Files :** Dont keep any of you applications,data inside of your image this will directly add to the image size.Instead,connect a container to and external storage volume and store your data over there so that its accessible by the application but also doesnt bloat the image. Alternatively your application could also connect to an external data store like MySQL or AWS S3 and access the data from there.
- **Use .dockerignore file:** Docker ignore similar to .gitignore. It lets you exclude specific files and directories from your final image.We can add .dockerignore file to the root of our project.For example, you could add large data files,virtual environment ,Logs, model checkpoints, and temporary files to your .dockerignore file.

```
data/
```
```
# Exclude virtual environmentvenv/# Exclude cache, logs, and temporary files__pycache__/*.log*.tmp*.pyc*.pyo*.pyd.pytest_cache.git.gitignoreREADME.md# Exclude model training checkpoints and tensorboard logscheckpoints/runs/
```

- **Leveraging Image Analysis Tools**: Image compression tools like `[Dive](https://github.com/wagoodman/dive)` and Docker slim are also very powerful. They will let you analyze each image layer including the layer size and what files are inside and can help you to figure out where is the dead weight and what you could remove.
- **Unikernels:** They are much smaller images which come packed with your application and underlying operating system designed to run directly,but require a deeper understanding to implement effectively.(Personally i have not tried it yet, but they can be 80% smaller than your typical docker image)

## Essential Security Practices for Slimming Down Docker Images Safely:

- Use **Trusted and Official** Base Images.Avoid unverified images from unknown sources.
- Always Run Containers as **Non-Root Users**

```
RUN adduser --disabled-password --gecos "" appuserUSER appuser
```

- Limit the network exposure of your container by **restricting the ports and IP addresses**

```
docker run -p 127.0.0.1:8080:8080 myimage
```

Regularly **scan your Docker images** for known vulnerabilities.(Consider using tools like [**Trivy**](https://github.com/aquasecurity/trivy) to regularly scan your images for vulnerabilities.)

```
docker scan your-image:tag
```

- **Avoid hardcoding sensitive information** like API keys or passwords directly into your Dockerfile or environment variables.Instead use methods like Docker secrets or environment variables managed by orchestration tools
- **Enable Logging and Monitoring** for containers to track any suspicious activities

## Conclusion

After implementing these techniques, here’s what we achieved:

- **Image Size**: Reduced from 1.2GB to 8MB (99.33% reduction)
- **Deployment Time**: Cut by 85%
- **Cloud Costs**: Reduced by 60%

Remember, the key is to start with a minimal base image, use multi-stage builds to separate your build environment from your runtime environment, and continually optimize your layers and dependencies. With these methods, you too can achieve significant reductions in your Docker image sizes!

I encourage you to try these optimization techniques in your own projects. Start with multi-stage builds, then progressively apply the other techniques to see how small and efficient you can make your Docker images. Happy optimizing :)