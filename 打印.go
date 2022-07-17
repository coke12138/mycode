package main // 声明代码所属的包

import ( // 所需要使用的包
	"fmt"
	"math/rand"
)

func main() { // 程序从main包的main函数开始执行

	spaceline := [3]string{"Space Adventures", "SpaceX", "Virgin Galactic"}
	triptype := [2]string{"One-Way", "Round-trip"}
	fmt.Printf("%-17v %-4v %-10v %-5v\n", "Spaceline", "Days", "Trip type", "Price")
	fmt.Println("========================================")
	for i := 0; i < 10; i++ {
		sp := spaceline[rand.Intn(3)]
		day := 62100000 / (rand.Intn(14) + 16) / (3600 * 24)
		ttype := triptype[rand.Intn(2)]
		price := rand.Intn(5000-3600) + 3600
		fmt.Printf("%-17v %-4v %-10v %-5v$\n", sp, day, ttype, price)
	}
}
