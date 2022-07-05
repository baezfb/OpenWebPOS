from openwebpos import OpenWebPOS

application = OpenWebPOS()

if __name__ == '__main__':
    try:
        application.run()
    except RecursionError as re:
        print("Unable to start OpenWebPOS. Please check your configuration.")
        print("Error/s:" + str(re))
