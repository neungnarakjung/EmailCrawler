"""
The MIT License (MIT)

Copyright (c) 2014 Ankit Aggarwal <ankitaggarwal011@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sys
import urllib

to_search_list = []
searched_list = []

def download(max_iterations):

    iteration = 1
    while iteration <= int(max_iterations):

        print "Searching for emails..."
        print "Number of sites searched: %s" % len(searched_list)

        ## We reached a dead end if there are no
        ## more sites in our to_search_list

        if len(to_search_list) == 0:
            print "Dead URL end"
            break

        ## Get the first URL from the list of the URLs
        ## we need to crawl over, and place it in the list
        ## of URLs that we already crawled.

        first_url = to_search_list[0]
        to_search_list.remove(first_url)
        searched_list.append(first_url)

        ## A simple function using urllib to download
        ## a URL

        def download_url(url):
            return urllib.urlopen(url)

        ## Try to download the URL. In case of an error,
        ## forget about it and move on to the next URL.

        try:
            content = download_url(first_url)
        except:
            try:
                content = download_url(first_url)
            except:
                iteration += 1
                continue

        for line in content:

            ## Find more URLs
            import re

            ## The regular expression we will use to search for URLs:
            url_expression= r'http://+[\w\d:#@%/;$()~_?\+-=\\\.&]*'
            regex = re.compile(url_expression)

            ## Find all the URLs and

            results = regex.findall(line)
            if results:
                for result in results:

            ## If the URL is new, add it to the list
            ## of URLs we need to crawl over.
                    if result not in searched_list:
                        to_search_list.append(result)

        iteration += 1


def output_results():

    ## This function will print the following information:
    ## number of sites in our sites to crawl list, the number
    ## of sites we actually crawled, and the total number of
    ## emails collected.

    print "Number of sites to search: %s" % len(to_search_list)
    print "Number of sites searched: %s" % len(searched_list)
    entry = ''
    for url in to_search_list:
        entry = entry + url + '\n'
    print entry


def write_results():

    ## Write all the information that the
    ## output_results() function prints out (see above)
    ## into a file called "info.txt"

    info_file_name = "info.txt"
    i = open("info.txt", "w")     ## create the file
    i.write("Number of sites to search: %s \n" % len(to_search_list))
    i.write("Number of sites searched: %s \n" % len(searched_list))
    i.close()

    ## Write down all the emails collected into a file called
    ## "email_addresses.txt". We will use this file in the next
    ## part of this example.

    file_name = "url_to_search.txt"
    n = open(file_name, "w")

    for url in to_search_list:
        n.write(url+'\n')

    n.close()


def get_input():

    ## Gather input from the user using sys.argv

    try:
        filename = sys.argv[1]
    except:
        raise Exception("\n\nSorry, invalid input. Please enter one arguments: the website URL.\n")

    return filename

def main():
    filename = get_input()
    with open(filename) as f:
        content = f.readlines()
    for i in content:
        urltosearch = i.rstrip('\n').lstrip(' ')
        to_search_list.append(urltosearch)
    iterations = len(to_search_list)
    download(iterations)
    if len(to_search_list) > 0 :
        output_results()
        write_results()


if __name__ == "__main__":
    main()
