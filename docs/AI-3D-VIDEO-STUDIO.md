# Dreamotion AI — 3D Video Studio

This is an additive first milestone inside the existing Dreamotion AI repository. Existing image-to-video files are not replaced.

## First milestone
A real 10-second procedural 3D animation rendered by Blender, with animated 3D geometry, moving camera, lighting, compositor glow, title text, and an original generated ambient audio bed. The workflow uploads the MP4 and editable Blender scene as a GitHub Actions artifact.

## Run in GitHub
1. Open **Actions** in the repository.
2. Select **Render Dreamotion 3D prototype**.
3. Choose **Run workflow**, enter a short topic, and start it.
4. Open the completed run and download the **Dreamotion-3D-Prototype** artifact.

## Render locally
Install Blender and FFmpeg, then run:
```bash
mkdir -p output
STUDIO_TOPIC="DREAMOTION AI" OUTPUT_DIR=output blender -b --python engine/blender/prototype_10s.py
bash scripts/make_audio.sh output
```

## Notes
- The first milestone is a procedural motion-graphics scene, not a rigged human character.
- GitHub-hosted runners render on CPU; render time depends on runner availability.
- The MP4 is an Actions artifact, not automatically published to a public URL.
- Keep generated media in output/; do not commit large renders to Git.
- No paid APIs or external AI model keys are required for this initial render.
