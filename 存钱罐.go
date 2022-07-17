package main // 声明代码所属的包
import (
	"fmt"
	"math/rand"
)

// 所需要使用的包

func main() { // 程序从main包的main函数开始执行
	f := [3]float32{0.05, 0.10, 0.25}
	var s float32 = 0.0
	for {
		add := f[rand.Intn(3)]
		s += add
		fmt.Printf("%-5.2f (+%-4.2f)\n", s, add)
		if s >= 20 {
			break
		}
	}
}
