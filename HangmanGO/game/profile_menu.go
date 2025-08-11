package game

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"HangmanGO/profiles"
)

func authenticateOrCreateProfile() *profiles.Profile {
	reader := bufio.NewReader(os.Stdin)
	for {
		profilesList, _ := profiles.ListProfiles()
		if len(profilesList) == 0 {
			fmt.Println("No profiles. Create one.")
			return createProfilePrompt(reader)
		}
		fmt.Println("Profiles:")
		for i, p := range profilesList {
			fmt.Printf("%d. %s\n", i+1, p)
		}
		fmt.Print("Select profile, or type 'create' to make new: ")
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)
		if choice == "create" || choice == "new" {
			return createProfilePrompt(reader)
		}
		idx := -1
		for i, p := range profilesList {
			if choice == p || choice == fmt.Sprintf("%d", i+1) {
				idx = i
				break
			}
		}
		if idx == -1 {
			fmt.Println("Invalid.")
			continue
		}
		fmt.Print("Password: ")
		password, _ := reader.ReadString('\n')
		password = strings.TrimSpace(password)
		profile, err := profiles.AuthenticateProfile(profilesList[idx], password)
		if err != nil {
			fmt.Println("Wrong password.")
			continue
		}
		fmt.Printf("Welcome, %s!\n", profile.Name)
		return profile
	}
}

func createProfilePrompt(reader *bufio.Reader) *profiles.Profile {
	for {
		fmt.Print("New profile name: ")
		name, _ := reader.ReadString('\n')
		name = strings.TrimSpace(name)
		if name == "" || strings.ContainsAny(name, "/\\:*?\"<>|") {
			fmt.Println("Invalid name.")
			continue
		}
		profilesList, _ := profiles.ListProfiles()
		for _, p := range profilesList {
			if p == name {
				fmt.Println("Profile exists.")
				continue
			}
		}
		fmt.Print("Password: ")
		password, _ := reader.ReadString('\n')
		password = strings.TrimSpace(password)
		fmt.Print("Confirm: ")
		confirm, _ := reader.ReadString('\n')
		confirm = strings.TrimSpace(confirm)
		if password != confirm {
			fmt.Println("Passwords do not match.")
			continue
		}
		profile, err := profiles.CreateProfile(name, password)
		if err != nil {
			fmt.Println("Error creating profile:", err)
			continue
		}
		fmt.Printf("Profile '%s' created!\n", name)
		return profile
	}
}
