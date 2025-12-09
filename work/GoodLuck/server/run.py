

# import sys
# print("Python路径:", sys.path)
# print("当前目录:", __file__)

import app


app=app.create_app()
if __name__ == '__main__':

    app.run(host='0.0.0.0')
