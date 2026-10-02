from yagbu.runtime import StreamingRuntime


def main() -> None:
    runtime = StreamingRuntime(model_dir="./models")
    print(runtime.generate("Hello from YAGBU"))


if __name__ == "__main__":
    main()
