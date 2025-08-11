package profiles

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
)

const (
	profileDir  = "profiles"
	profileExt  = ".json"
)

type Profile struct {
	Name     string            `json:"name"`
	Password string            `json:"password"`
	Balance  int               `json:"balance"`
	Inventory map[string]int   `json:"inventory"`
}

func ensureProfileDir() error {
	return os.MkdirAll(profileDir, 0755)
}

func ListProfiles() ([]string, error) {
	if err := ensureProfileDir(); err != nil {
		return nil, err
	}
	files, err := os.ReadDir(profileDir)
	if err != nil {
		return nil, err
	}
	var profiles []string
	for _, f := range files {
		if !f.IsDir() && filepath.Ext(f.Name()) == profileExt {
			profiles = append(profiles, f.Name()[:len(f.Name())-len(profileExt)])
		}
	}
	return profiles, nil
}

func profilePath(name string) string {
	return filepath.Join(profileDir, name+profileExt)
}

func SaveProfile(p *Profile) error {
	if err := ensureProfileDir(); err != nil {
		return err
	}
	f, err := os.Create(profilePath(p.Name))
	if err != nil {
		return err
	}
	defer f.Close()
	return json.NewEncoder(f).Encode(p)
}

func LoadProfile(name string) (*Profile, error) {
	f, err := os.Open(profilePath(name))
	if err != nil {
		return nil, err
	}
	defer f.Close()
	var p Profile
	if err := json.NewDecoder(f).Decode(&p); err != nil {
		return nil, err
	}
	if p.Inventory == nil {
		p.Inventory = make(map[string]int)
	}
	return &p, nil
}

func DeleteProfile(name string) error {
	return os.Remove(profilePath(name))
}

func AuthenticateProfile(name, password string) (*Profile, error) {
	p, err := LoadProfile(name)
	if err != nil {
		return nil, err
	}
	if p.Password != password {
		return nil, errors.New("wrong password")
	}
	return p, nil
}

func CreateProfile(name, password string) (*Profile, error) {
	if name == "" {
		return nil, errors.New("empty name")
	}
	if password == "" {
		return nil, errors.New("empty password")
	}
	p := &Profile{
		Name:     name,
		Password: password,
		Balance:  0,
		Inventory: make(map[string]int),
	}
	if err := SaveProfile(p); err != nil {
		return nil, err
	}
	return p, nil
}

func PrintProfiles() {
	profiles, err := ListProfiles()
	if err != nil {
		fmt.Println("Error listing profiles:", err)
		return
	}
	fmt.Println("Profiles:")
	for i, p := range profiles {
		fmt.Printf("%d. %s\n", i+1, p)
	}
}
