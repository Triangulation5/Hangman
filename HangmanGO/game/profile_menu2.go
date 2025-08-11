package game

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"HangmanGO/profiles"
)

func ProfileMenu(current *profiles.Profile) *profiles.Profile {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Printf("\nPROFILE MENU (Current: %s)\n", current.Name)
		fmt.Println("1. Change profile")
		fmt.Println("2. New profile")
		fmt.Println("3. Delete profile")
		fmt.Println("4. Exit menu")
		fmt.Print("Option: ")
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(strings.ToLower(choice))
		switch choice {
		case "1", "change":
			return authenticateOrCreateProfile()
		case "2", "create", "new":
			return createProfilePrompt(reader)
		case "3", "delete":
			if deleteProfilePrompt(reader) {
				return authenticateOrCreateProfile()
			}
		case "4", "exit", "q":
			return current
		default:
			fmt.Println("Invalid.")
		}
	}
}

func deleteProfilePrompt(reader *bufio.Reader) bool {
	profilesList, _ := profiles.ListProfiles()
	if len(profilesList) == 0 {
		fmt.Println("No profiles to delete.")
		return false
	}
	for {
		fmt.Println("Profiles:")
		for i, p := range profilesList {
			fmt.Printf("%d. %s\n", i+1, p)
		}
		fmt.Print("Select profile to delete #: ")
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(choice)
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
		fmt.Printf("Type '%s' to confirm deletion: ", profilesList[idx])
		confirm, _ := reader.ReadString('\n')
		confirm = strings.TrimSpace(confirm)
		if confirm == profilesList[idx] {
			profiles.DeleteProfile(profilesList[idx])
			fmt.Printf("Profile '%s' deleted.\n", profilesList[idx])
			return true
		} else {
			fmt.Println("Deletion cancelled.")
			return false
		}
	}
}
