package game

import (
	"fmt"
	"HangmanGO/asciiart"
)

func ShowInventory(inventory map[string]int) {
	fmt.Println(asciiart.InventoryBanner)
	if len(inventory) == 0 {
		fmt.Println("No items.")
		return
	}
	idx := 1
	for item, count := range inventory {
		desc := ""
		for _, shopItem := range ShopItems {
			if shopItem.Name == item {
				desc = shopItem.Desc
				break
			}
		}
		fmt.Printf("%d. %s x%d - %s\n", idx, item, count, desc)
		idx++
	}
	fmt.Printf("%d. Exit\n", idx)
}
