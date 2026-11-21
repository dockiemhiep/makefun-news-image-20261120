import os
import shutil


def main() -> None:
    source_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(source_dir, "entry.png"),
        os.path.join(output_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
