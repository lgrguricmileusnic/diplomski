package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/charmbracelet/bubbles/progress"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

const (
	padding  = 2
	maxWidth = 80
)

type responseMsg struct {
	Speed    float64
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

func waitForActivity(sub chan responseMsg) tea.Cmd {
	return func() tea.Msg {
		return responseMsg(<-sub)
	}
}

type model struct {
	sub      chan responseMsg
	speed    float64
	blinkers bool
	quitting bool
	progress progress.Model
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

	case tea.WindowSizeMsg:
		m.progress.Width = msg.Width - padding*2 - 4
		if m.progress.Width > maxWidth {
			m.progress.Width = maxWidth
		}
		return m, nil

	case responseMsg:
		m.speed = msg.Speed
		m.blinkers = msg.Blinkers
		return m, waitForActivity(m.sub)

	case progress.FrameMsg:
		progressModel, cmd := m.progress.Update(msg)
		m.progress = progressModel.(progress.Model)
		return m, cmd

	default:
		return m, nil
	}
}

func (m model) View() string {
	// s := fmt.Sprintf("\n Current speed: %f Blinkers: %t\n\n Press any key to exit\n", m.speed, m.blinkers)
	pad := strings.Repeat(" ", padding)
	return "\n" +
		pad + m.progress.ViewAs(m.speed) + "\n\n" +
		pad + "Press any key to quit"
}

func main() {
	pm := progress.New(progress.WithSolidFill("#FF2800"))
	pm.PercentageStyle.AlignVertical(lipgloss.Center)
	pm.PercentFormat = "%f km/h"
	p := tea.NewProgram(model{
		sub:      make(chan responseMsg),
		blinkers: false,
		speed:    0.0,
		progress: pm},
		tea.WithAltScreen())

	if _, err := p.Run(); err != nil {
		fmt.Println("could not start program:", err)
		os.Exit(1)
	}
}
