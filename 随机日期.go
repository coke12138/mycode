package main // 声明代码所属的包

import ( // 所需要使用的包
	"fmt"
	"math/rand"
)

var era = "AD"

func main() { // 程序从main包的main函数开始执行

	for i := 0; i < 10; i++ {
		year := rand.Intn(25) + 2000
		month := rand.Intn(12) + 1
		daysInMonth := 31

		switch month {
		case 2:
			if year%4 == 0 {
				daysInMonth = 29
			} else {
				daysInMonth = 28
			}
		case 4, 6, 9, 11:
			daysInMonth = 30
		}

		day := rand.Intn(daysInMonth) + 1

		fmt.Println(era, year, month, day)
	}

}
