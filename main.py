from modules.controller import *
from modules.view import view_func


if __name__ == '__main__':
    
    main()

    while True:
    
        requests_func = view_func()

        if requests_func[2] is exit_:

            sub_func = requests_func[2]()

        elif requests_func[1] == 'lower':

            sub_func = requests_func[2](target_file_path)

            if sub_func[1] == 'top':
                continue