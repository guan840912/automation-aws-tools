import sys
import configparser

def main(value: str):
  print('hello world {}'.format(value))

if __name__ == "__main__":
    action = 'stop' if len(sys.argv) == 1 else sys.argv[1:]
    print(action)
    #main(action[1])