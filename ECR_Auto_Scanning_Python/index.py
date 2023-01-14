from json import loads, dumps
import json
import subprocess
import csv

class Vulnurability:
    repo_name: str = ""
    pack_name: str = ""
    pack_version: str = ""
    image_id: str = ""
    uri: str = ""

repos = []
list_critical = []
findings = []

def get_all_repos():
    get_repos = subprocess.Popen("aws ecr describe-repositories", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    json_repo_result = json.loads(get_repos.stdout.read())
    repositories = json_repo_result["repositories"]
    print(f'Number of repos: {len(repositories)}')
    return repositories

def get_latest_img_digest(repo_name):
    get_latest_image_cmd = f"aws ecr describe-images --repository-name  {repo_name}  --query 'sort_by(imageDetails,& imagePushedAt)[-1].imageDigest'"
    get_latest_image = subprocess.Popen(get_latest_image_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    image_Digest = get_latest_image.stdout.read().decode('utf-8') 
    #print(f'image_Digest: {image_Digest}')
    return image_Digest

def start_scanning(repo_name, image_Digest):
    start_scan_cmd = f"aws ecr start-image-scan --repository-name {repo_name} --image-id imageDigest={image_Digest}"
    start_scan = subprocess.Popen(start_scan_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    scan_result = start_scan.stdout.read().decode('utf-8')
    # print(f'scan_result: {scan_result}')
    return scan_result

def wait_scan_results(repo_name, image_Digest):
    wait_scan_cmd = f"aws ecr wait image-scan-complete --repository-name {repo_name} --image-id imageDigest={image_Digest}"
    wait_scan = subprocess.Popen(wait_scan_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    wait_scan.stdout.read().decode('utf-8')

def get_scan_result(repo_name, image_Digest):
    cmd_finding = f"aws ecr describe-image-scan-findings --repository-name {repo_name} --image-id imageDigest={image_Digest}"
    get_findings = subprocess.Popen(cmd_finding, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    result = json.loads(get_findings.stdout.read())
    return result

def finding_vulnarablity(repo_name, json_finding_result):
    print_to_json( json_finding_result['imageScanFindings']['findings'])
    for result in json_finding_result['imageScanFindings']['findings']:      
        if(result['severity'] == "CRITICAL"):
            item  = Vulnurability()
            item.repo_name = repo_name
            item.uri = result['uri']
            list_critical.append(item)
            attributes = result['attributes']

            for att in attributes:                    
                if(att["key"] == "package_name"):
                    item.pack_name = att["value"]
                if(att["key"] == "package_version"):
                    item.pack_version = att["value"]

def write_to_csv(list_critical):
    if(len(list_critical) > 0):
        csv_columns = ["Repo","package_name","version","uri"]
        with open("repo_with_CRITICAL_issues.csv", 'w', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_columns)
            for ob in list_critical:  
                row = [ob.repo_name, ob.pack_name,ob.pack_version,ob.uri]        
                writer.writerow(row)

def print_to_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

def main():
    # get all the repos
    repositories = get_all_repos()

    for repo in repositories:
        repo_name = repo["repositoryName"]
        print(f" --> repo_name: {repo_name}")
        print (f'------------- Starting scanning : {repo_name}')

        # get latest image for the repo
        image_Digest = get_latest_img_digest(repo_name)       

        print(f'------------- Started the scanning: {repo_name}')
        start_scanning(repo_name, image_Digest)
    
        # waiting scan result
        print(f'------------- Waiting to finish the scanning: {repo_name}')
        wait_scan_results(repo_name, image_Digest)
        
        # get scan results
        json_finding_result = get_scan_result(repo_name, image_Digest)

        status = json_finding_result['imageScanStatus']['status']
        print(f'Status of scan: {status}')
        if(status == "FAILED"):
            print(f'>>>>>>>>>>>>>>>>>>>Failed to scan the repo: {repo_name}')
            continue
    
        # finding vulnarabilities 
        finding_vulnarablity(repo_name, json_finding_result)

        # write all critical issues to csv file
        write_to_csv(list_critical)

    print(f'Repos with issues: {len(list_critical)}')
    print(f'=====================================================') 

if __name__ == "__main__":
    main()

