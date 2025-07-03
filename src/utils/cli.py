def print_logo():
    print("███████╗ █████╗ ███████╗███████╗███████╗██╗   ██╗███╗   ██╗ ██████╗")
    print("██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝")
    print("███████╗███████║█████╗  █████╗  ███████╗ ╚████╔╝ ██╔██╗ ██║██║     ")
    print("╚════██║██╔══██║██╔══╝  ██╔══╝  ╚════██║  ╚██╔╝  ██║╚██╗██║██║     ")
    print("███████║██║  ██║██║     ███████╗███████║   ██║   ██║ ╚████║╚██████╗")
    print("╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚═════╝")

def print_help():
    print_logo()
    print(f"Usage: safesync <command> [<args>]")
    print("===")
    print("Available commands:")
    print("safesync init")
    print("safesync status")
    print("safesync snap")
    print("safesync states")
    print("safesync restore <state_id>")
