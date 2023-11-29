/*
	Program:	urlplay.go
	Date:		29-Oct-2013
	Version:	0.3.1
	
	Purpose:	I'm playing with URL parsing, as a prelude to building a full blown URL switcher
					for a web application that will handle multiple domains.

	Copyright (c) 2013 Dale Weber <hybotics.pdx@gmail.com, @hybotics on App.net and Twitter>

	ALL RIGHTS RESERVED
*/
package main

import (
	"fmt"
	"log"
	"errors"
	"strings"
	"net/url"
)

// Create the full url from the parts of the URL struct
func MakeURL (u *url.URL) (ur string) {
	ur = u.Scheme + "://" + u.Host + u.Path + "?" + u.RawQuery

	return
}

// Display the data from the URL struct
func showURL (u *url.URL, st string) {
	fmt.Printf("\n%s:\n\n", st)

	us := MakeURL(u)

	fmt.Printf("URL:      %s\n", us) 
	fmt.Printf("Path:     %s\n", u.Path)
	fmt.Printf("Host:     %s\n", u.Host)
	fmt.Printf("Scheme:   %s\n", u.Scheme)
	fmt.Printf("Raw Q:    %s\n", u.RawQuery)
	fmt.Printf("Fragment: %s\n", u.Fragment)
	fmt.Printf("User:     %s\n", u.User)
}

/*
	Cuts the host part of a URL into a prefix and domain slice, based on the number
		of domain parts wanted.
*/
func splitHost (hostPart string, nrDomain int) (prefix, domain []string, err error) {
	var checkLen int

	err = nil											// Assume everything will go well for now

	host := strings.Split(hostPart, ".")				// Split the host part of the URL

	// The number of parts in the host slice
	nrHost := len(host)

	fmt.Printf("Length of host[0] = %d, nrHost = %d\n", len(host[0]), nrHost)

	// Check the lengths of the host slice elements to make sure they are > 0
	for index := range host {
		checkLen = len(host[index])
		
		if checkLen == 0 {
			break										// We have a 0 length element, no need to continue
		}
	}

	prefix = nil										// We won't necessarily have a prefix part

	// Validate the URL and break it into prefix and domain parts if it's valid
	if checkLen > 0 && nrHost == 2 {					// There is no prefix, just the domain (hybotics.org)
		domain = host
	} else if nrHost > nrDomain && nrDomain > 0 {		// We have a prefix and a domain part (www, hybotics.org)
		prefix = host[0 : nrHost - nrDomain]
		domain = host[nrHost - nrDomain :]
	} else {											// The URL.Host, or number of domain parts is invalid
		domain = nil

		// Set the appropriate error message
		if nrHost < 2 || checkLen == 0 {
			err = errors.New(fmt.Sprintf("You have an invalid host: %s!\n", hostPart))
		} else if nrDomain < 1 || nrDomain > nrHost {
			err = errors.New(fmt.Sprintf("The number of domain parts (%d) wanted is out of range!\n", nrDomain))
		} else {
			err = errors.New(fmt.Sprintf("Unhandled error in func splitHost(%s, %d)!\n", hostPart, nrDomain))
		}
	}

	return
}

func main() {
	var domain, prefix []string
	
	/*
		This is slightly modified code from the original example
	*/

	u, err := url.Parse("http://www.bing.com/search?q=dotnet")

	if err != nil {
		log.Fatal(err)
	}

	showURL(u, "Before")
	
	u.Scheme = "https"
	u.Host = "www.walter.robots.hybotics.org"
	u.Path = "/find"
	
	q := u.Query()
	q.Set("q", "walter")

	u.RawQuery = q.Encode()

	showURL(u, "After")

	/*
		End modified original code
	*/
	
	fmt.Printf("\nhost = %q\n", u.Host)

	// The number of domain parts must be > 0 and <= the number of parts of the URL.Host
	prefix, domain, err = splitHost(u.Host, 2)
	
	if err != nil {
		log.Fatal(err)
	} else {											// Make sure we have a valid domain before continuing
		fmt.Printf("prefix = %q, domain = %q\n", prefix, domain)
	}
}
