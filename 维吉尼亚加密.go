//凯撒加密变种，密钥是一个单词
package main // 声明代码所属的包
import (
	"fmt"
	"strings"
)

// 所需要使用的包

func main() { // 程序从main包的main函数开始执行
	keyword := "GOLANG"
	message := "Get Programming with Go!!123"
	message = strings.ToUpper(message)
	//fmt.Scanln(&message)
	//length := utf8.RuneCountInString(message)
	fmt.Println("你的输入是：\n" + message)
	var result string
	j := 0
	for _, c := range message {
		//fmt.Printf("%c", c)
		if c >= 'A' && c <= 'Z' {
			//fmt.Printf("%c - %c - %c - %c\n", c, keyword[j], c+rune(keyword[j]), c+rune(keyword[j])-26)
			newone := c + rune(keyword[j]) - 'A'
			//fmt.Printf(" newone = %c ", newone)
			if newone > 'Z' {
				newone -= 26
			}
			//fmt.Printf(" newone = %c\n", newone)
			//fmt.Printf("key: %c\n", keyword[j])
			//message = strings.Replace(message, string(c), string(newone), 1)
			j++
			if j > len(keyword)-1 {
				j = 0
			}
			result += string(newone)
		} else {
			result += string(c)
		}

	}
	fmt.Println()
	fmt.Println(result)
}
