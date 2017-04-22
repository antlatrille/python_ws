from api import Api_v1
from bottle import run, Bottle

v1 = Api_v1()

main = Bottle()
main.mount('/1', v1)
run(main, host='localhost', port=8080, server='tornado')