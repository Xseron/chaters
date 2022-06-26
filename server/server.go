package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
)

type User struct {
	name string
	pass string
	is_loged bool
	now_seccion net.Conn
}

var users = make([]User,0)

func new_connection(conn net.Conn)  {
	for {
		buf := make([]byte, 1024)
		n, err := conn.Read(buf)
		if err!=nil{
			for _,v := range users{
				if v.now_seccion == conn{
					v.is_loged = false
					v.now_seccion = nil
				}
			}
			return
		}
		if n!=0 {
			var dat map[string]interface{}
			json.Unmarshal(buf[:n], &dat)
			user_name := dat["user_name"].(string)
			message_type := dat["type"].(string)
			d:
			switch message_type {
			case "REGISTER":
				pass := dat["password"].(string)
				for _, v := range users {
					if v.name == user_name{
						conn.Write([]byte("NAME_EMPLOYED_ERROR"))
						break d
					}
				}
				users = append(users, User{user_name, pass, true, conn})
				conn.Write([]byte("REGISTERED"))

			case "LOGIN":
				pass := dat["password"].(string)
				for _, v := range users {
					if v.name == user_name && v.pass == pass {
						v.is_loged = true
						v.now_seccion = conn
						conn.Write([]byte("LOGIN"))
						break d
					}
				}
				conn.Write([]byte("LOGIN_ERROR"))

			case "MESSAGE":
				message := dat["message"].(string)
				for _,v := range users{
					if v.now_seccion!=nil && v.now_seccion!=conn {
						v.now_seccion.Write([]byte(message))
					}
				}
				conn.Write([]byte("SENDED"))
			}
			fmt.Println(users)
		}
	}
}

func main() {
	const addr = "localhost:8080"
	server, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalln(err)
	}
	defer server.Close()

	log.Println("Server is running on:", addr)

	for {
		conn, err := server.Accept()
		if err != nil {
			log.Println("Failed to accept conn.", err)
			continue
		}

		go new_connection(conn)
	}
}