package main

import (
	"bufio"
	"encoding/binary"
	"fmt"
	"math/rand"
	"os"
	"reflect"
	"strconv"
	"strings"
	"time"
)

func getCurrentDraw() ([]uint8, int64) {

	// take the input
	fmt.Println("# Connect to 'c.ctf.turtleturtleup.com:1339' and enter some guess")
	fmt.Println("# Wait for the draw to happen and copy the result")
	fmt.Println("# Something like: '25 13 106 174 234 30' (no brackets or quote)")
	fmt.Println("# It needs to be from the current minute or it will not work:")
	reader := bufio.NewReader(os.Stdin)

	t, _ := reader.ReadString('\n')

	// remove the nasty carriage return
	t = strings.Replace(t, "\n", "", -1)
	t1 := strings.Fields(t)

	var currentDraw = []uint8{}
	// convert it from a flat string to a slice of uint8
	for _, i := range t1 {
		j, err := strconv.Atoi(i)
		if err != nil {
			panic(err)
		}
		currentDraw = append(currentDraw, uint8(j))
	}

	// grab the current unix time (rounded to the nearest minute)
	var currentTime int64
	currentTime = time.Now().Truncate(time.Minute).Unix()

	return currentDraw, currentTime

}

func getCurrentSeed(currentDraw []uint8, currentTime int64) int64 {

	fmt.Println("# One moment, calculating")

	// We know the seed must be between 1 and 999999, so lets loop through
	for globalSeed := 1; globalSeed <= 999999; globalSeed++ {
		//fmt.Println(globalSeed)

		draw := make([]uint8, 6)

		r := rand.New(rand.NewSource(int64(globalSeed) + currentTime))
		binary.Read(r, binary.LittleEndian, &draw)

		// if it matches, we have found the seed
		if reflect.DeepEqual(draw, currentDraw) {
			fmt.Print("The globalSeed is: ")
			fmt.Println(globalSeed)
			return int64(globalSeed)

		}

	}

	return 0
}

func predictNext(globalSeed int64) {

	draw := make([]uint8, 6)

	fmt.Println("The next balls are: ")

	// guess the next 3 draws
	times := []int64{60, 120, 180} //60 second increments
	for _, t := range times {

		// Add the times to the current time to predict the future
		r := rand.New(rand.NewSource(globalSeed + time.Now().Truncate(time.Minute).Unix() + t))
		binary.Read(r, binary.LittleEndian, &draw)

		fmt.Println(draw)

	}
}

func main() {
	// take input of the current balls
	currentDraw, currentTime := getCurrentDraw()

	// Work out the current seed based on the time and last draw
	globalSeed := getCurrentSeed(currentDraw, currentTime)

	// predict the next balls
	predictNext(globalSeed)

}
