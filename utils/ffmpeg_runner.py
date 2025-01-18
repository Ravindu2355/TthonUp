import asyncio

async def run_ffmpeg(input_path, output_path, progress):
    cmd = f"ffmpeg -i {input_path} -c:v libx264 -preset fast -c:a aac {output_path}"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    while True:
        output = await process.stderr.readline()
        if not output:
            break
        await progress.update(output.decode("utf-8").strip())

    await process.wait()
