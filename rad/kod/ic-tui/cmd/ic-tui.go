package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	tea "github.com/charmbracelet/bubbletea"
)

type responseMsg struct {
	Speed    float32
	Blinkers bool
}

func listenForActivity(sub chan responseMsg) tea.Cmd {
	return func() tea.Msg {
		for {
			mux := http.NewServeMux()
			mux.HandleFunc("POST /update", func(w http.ResponseWriter, r *http.Request) {

				var msg responseMsg

				err := json.NewDecoder(r.Body).Decode(&msg)

				if err != nil {
					http.Error(w, err.Error(), http.StatusBadRequest)
					return
				}

				sub <- msg
			})
			http.ListenAndServe(":8080", mux)
		}
	}
}

// A command that waits for the activity on a channel.
func waitForActivity(sub chan responseMsg) tea.Cmd {
	return func() tea.Msg {
		return responseMsg(<-sub)
	}
}

type model struct {
	sub      chan responseMsg
	speed    float32
	blinkers bool
	quitting bool
}

func (m model) Init() tea.Cmd {
	return tea.Batch(
		listenForActivity(m.sub),
		waitForActivity(m.sub),
	)
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		m.quitting = true
		return m, tea.Quit
	case responseMsg:
		m.speed = msg.Speed
		m.blinkers = msg.Blinkers

		return m, waitForActivity(m.sub) // wait for next event
	default:
		return m, nil
	}
}

func (m model) View() string {
	s := fmt.Sprintf("\n Current speed: %f Blinkers: %t\n\n Press any key to exit\n", m.speed, m.blinkers)
	if m.quitting {
		s += "\n"
	}
	return s
}

func main() {
	p := tea.NewProgram(model{
		sub: make(chan responseMsg),
	})

	if _, err := p.Run(); err != nil {
		fmt.Println("could not start program:", err)
		os.Exit(1)
	}
}
