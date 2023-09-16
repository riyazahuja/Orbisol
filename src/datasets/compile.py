import json





def generateDict(files):
    result = {}
    for file in files:
        with open(f'TLE/{file}.txt') as f:
            lines = f.readlines()
        raw_data = {}
        i=0
        while i in range(len(lines)):
            s = f"{lines[i]}{lines[i+1]}{lines[i+2]}"
            raw_data[lines[i]] = s
            i+=3
        

        result[file] = raw_data
    print(result)
    return result



def main():
    files = ['active','analyst','brightest','china','cosmos2251','iridium33','recent','russian','stations']
    output = generateDict(files)

    with open("final.json", "w") as outfile:
        outfile.write(json.dumps(output))


if __name__ == '__main__':
    main()