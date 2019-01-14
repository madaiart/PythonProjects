def main():
    import subprocess
    import os

    directory = '/path/.zip'

    lines = [line.rstrip('\n') for line in open('/path dictionary/')]
    for line in lines:
        subprocess.run(["7z", "e", "-aoa",directory, "-p", line])


if __name__ == '__main__':
    main() 
