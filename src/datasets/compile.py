import json
import re




def generateDict(files):
    result = {}
    cnts = {}
    for file in files:
        with open(f'TLE/{file}.txt') as f:
            lines = f.readlines()

        i=0
        while i in range(len(lines)):
            name = lines[i]
            name=name.rstrip()

            if name not in cnts.keys():
                cnts[name] = 0
            if name in cnts.keys() and cnts[name] > 0:
                name += f'({cnts[name]})'
            result[name] = {
                'line1' : lines[i+1],
                'line2' : lines[i+2]
            }
            i+=3
        

       
    #print(result)
    return result



def main():
    files = ['active','analyst','brightest','china','cosmos2251','iridium33','recent','russian','stations']
    output = generateDict(files)

    with open("final.json", "w") as outfile:
        outfile.write(json.dumps(output))


if __name__ == '__main__':
    main()