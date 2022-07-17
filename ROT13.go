func main() { // 程序从main包的main函数开始执行
	message := "Hola Estaci*n Espacial Internacional"

	for _, c := range message {
		//fmt.Printf("%c", c)
		if (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') {
			c += 13
			if (c > 'Z' && c < 'a') || c > 'z' {
				c -= 26
			}
		}

		fmt.Printf("%c", c)
	}
}
