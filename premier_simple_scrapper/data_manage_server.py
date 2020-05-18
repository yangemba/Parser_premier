"""description"""
import logging
import tornado.web as web
import tornado.ioloop
from utils.base_handler import RequestHandler


def setup_logging():
    logger = logging
    return logger


class DataFlowHandler(RequestHandler):
    """Handler for Managing files operations"""
    methods = ["POST"]

    async def post(self):
        """"
        POST method description
        """
        file_name = self.get_argument('file_name')
        if file_name is not None:
            self.finish(file_result)
            try:
                file_result = file_perform(file_name)
            except Exception as ex:
                self.logging.error(str(ex))



if __name__ == "__main__":
    application = tornado.web.Application(logging=setup_logging(),
                                          handlers=[(r"/",
                                                     DataFlowHandler)],
                                          )

    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
