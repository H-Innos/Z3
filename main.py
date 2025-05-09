import pytest

def main():
    pytest.main(["intervals"]) # this will take a couple of minutes to complete
    pytest.main(["def_exc"])

if __name__ == '__main__':
    main()

