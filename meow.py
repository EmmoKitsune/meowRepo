import argparse
import requests
import os
import stat

github_repo = "http://192.168.100.79/meow/"

def download_file(url, save_as):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_as, 'wb') as f:
            f.write(response.content)

        return True
    else:
        print(f"Error downloading package. Status code: {response.status_code}")
        return False

def get_package_file_name(package_name):

    response = requests.get(github_repo + "package-list.txt")
    if response.status_code == 200:
        
        package_list = response.content.decode('utf-8').splitlines()

        for line in package_list:
            name, file_name, type = line.split()
            if name == package_name:
                return file_name,type
            
        print(f"Package {package_name} not found in the list.")
        return None
    else:
        print(f"Error retrieving package list. Status code: {response.status_code}")
        return None


def install_package(package_name):

    file_name, type = get_package_file_name(package_name)
    if not file_name:
        return

    print(f"Downloading package {file_name}...")
    if download_file(github_repo + file_name, file_name):
        print(f"Package {file_name} downloaded!")

        match type:
            case "generic":
                print(f"Package {package_name} installed!")
            case "executable":
                os.chmod(file_name, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
                print(f"Package {package_name} installed!")
            case _:
                print("Cannot install package,unrecognized type.")

    else:
        print(f"Package {file_name} not found.")

def get_packages(_):
    response = requests.get(github_repo + "package-list-man.txt")
    if response.status_code == 200:
        print(response.content.decode('utf-8'))
    else:
        print(f"Error retrieving packages. Status code: {response.status_code}.")

def main():
    parser = argparse.ArgumentParser(description='Meow')
    
    #Args things
    parser.add_argument('order', type=str, choices=['owinstall', 'uwget'], help='Order to execute (owinstall, uwget)')

    parser.add_argument('package', type=str, nargs='?', default=None, help='Package name')
    
    
    args = parser.parse_args()
    
    order = args.order
    packageArg = args.package
    
    if order == 'owinstall' and packageArg is None:
        parser.error('Please enter a package name, type uwget to list all the packages')
    
    order_functions = {
        'owinstall': lambda pkg: install_package(pkg),
        'uwget': get_packages
    }
    
    # Execute the orders
    if order in order_functions:
        order_functions[order](packageArg)
    else:
        print("Order not found.")

if __name__ == '__main__':
    main()
