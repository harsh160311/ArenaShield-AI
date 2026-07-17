/* ============================================
   ArenaShield AI - Frontend Application
   ============================================ */

let sessionId = generateSessionId();
let autoRefresh = true;
let refreshInterval = null;
let selectedStadiumId = null;
let voiceRecognition = null;

function generateSessionId() {
    let stored = sessionStorage.getItem('arenashield_session');
    if (stored) return stored;
    let id = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    sessionStorage.setItem('arenashield_session', id);
    return id;
}

// ============================================
// STADIUM SELECTOR
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    initChat();
    initQuickActions();
    initEmergencyButton();
    initStadiumChangeButton();
    initDashboard();
    initVoiceInput();
    loadDefaultStadium();
});

function initVoiceInput() {
    const voiceBtn = document.getElementById('voiceBtn');
    if (!voiceBtn) return;

    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        voiceBtn.style.display = 'none';
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    voiceRecognition = new SpeechRecognition();
    voiceRecognition.continuous = false;
    voiceRecognition.interimResults = false;
    voiceRecognition.lang = 'en-US';

    voiceRecognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById('chatInput');
        if (input) {
            input.value = transcript;
            document.getElementById('chatForm').dispatchEvent(new Event('submit'));
        }
    };

    voiceRecognition.onerror = function() {
        voiceBtn.classList.remove('listening');
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    };

    voiceRecognition.onend = function() {
        voiceBtn.classList.remove('listening');
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    };

    voiceBtn.addEventListener('click', function() {
        if (voiceRecognition && !voiceBtn.classList.contains('listening')) {
            voiceBtn.classList.add('listening');
            voiceBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            try {
                voiceRecognition.start();
            } catch (e) {
                voiceBtn.classList.remove('listening');
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            }
        }
    });
}

function loadDefaultStadium() {
    var savedId = sessionStorage.getItem('arenashield_stadium');
    if (savedId) {
        selectStadium(savedId);
    } else {
        selectStadium('arenashield-national');
    }
}

function loadStadiums() {
    const results = document.getElementById('searchResults');
    if (!results) {
        return;
    }

    fetch('/api/stadiums')
    .then(function(r) { return r.json(); })
    .then(function(data) {
        window.allStadiums = data.stadiums;

        const searchInput = document.getElementById('stadiumSearch');
        const clearBtn = document.getElementById('clearSearchBtn');

        if (searchInput) {
            searchInput.addEventListener('input', function() {
                const q = this.value.trim();
                if (q.length === 0) {
                    results.innerHTML = '<div class="search-hint"><i class="fas fa-globe"></i><span>774+ stadiums — search or click "Use default stadium" below</span></div>';
                    if (clearBtn) clearBtn.style.display = 'none';
                    return;
                }
                if (clearBtn) clearBtn.style.display = 'block';

                const ql = q.toLowerCase();
                const filtered = data.stadiums.filter(function(s) {
                    return s.name.toLowerCase().includes(ql) ||
                           s.location.toLowerCase().includes(ql) ||
                           s.country.toLowerCase().includes(ql);
                });

                renderSearchResults(filtered, q);
            });

            searchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    this.value = '';
                    this.dispatchEvent(new Event('input'));
                    this.blur();
                }
                if (e.key === 'Enter') {
                    const first = document.querySelector('.search-result-item');
                    if (first) first.click();
                }
            });

            setTimeout(function() { searchInput.focus(); }, 400);
        }

        if (clearBtn) {
            clearBtn.addEventListener('click', function() {
                searchInput.value = '';
                searchInput.focus();
                searchInput.dispatchEvent(new Event('input'));
            });
        }
    })
    .catch(function() {
        results.innerHTML = '<div class="no-results">Could not load stadiums</div>';
    });

    const skipBtn = document.getElementById('skipStadiumBtn');
    if (skipBtn) {
        skipBtn.addEventListener('click', function() {
            selectStadium('arenashield-national');
        });
    }
}

function renderSearchResults(stadiums, query) {
    const results = document.getElementById('searchResults');
    if (!results) return;

    if (stadiums.length === 0) {
        results.innerHTML = '<div class="no-results">No stadiums match <strong>"' + escapeHtml(query) + '"</strong></div>';
        return;
    }

    var groups = {};
    stadiums.forEach(function(s) {
        var country = s.country || 'Other';
        if (!groups[country]) groups[country] = [];
        groups[country].push(s);
    });

    var sortedCountries = Object.keys(groups).sort();
    var html = '';
    var total = stadiums.length;

    html += '<div style="font-size:0.75rem;color:var(--text-light);padding:0.25rem 0.75rem 0.5rem;">' + total + ' stadium' + (total !== 1 ? 's' : '') + ' found</div>';

    sortedCountries.forEach(function(country) {
        html += '<div style="padding:0.25rem 0.75rem;font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:var(--accent);">' + country + ' <span style="color:var(--text-light);font-weight:400;">(' + groups[country].length + ')</span></div>';
        groups[country].forEach(function(s) {
            var nameHighlight = highlightMatch(s.name, query);
            var locHighlight = highlightMatch(s.location + ', ' + s.country, query);
            html += '<div class="search-result-item" tabindex="0" role="button" data-id="' + s.id + '">';
            html += '<div class="result-icon"><i class="fas fa-building"></i></div>';
            html += '<div class="result-info">';
            html += '<div class="result-name">' + nameHighlight + '</div>';
            html += '<div class="result-location">' + locHighlight + '</div>';
            html += '</div>';
            html += '<div class="result-country">' + s.country + '</div>';
            html += '</div>';
        });
    });
    results.innerHTML = html;

    document.querySelectorAll('.search-result-item').forEach(function(el) {
        el.addEventListener('click', function() {
            selectStadium(this.getAttribute('data-id'));
        });
        el.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                selectStadium(this.getAttribute('data-id'));
            }
        });
    });
}

function highlightMatch(text, query) {
    if (!query) return escapeHtml(text);
    var idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return escapeHtml(text);
    var before = escapeHtml(text.substring(0, idx));
    var match = escapeHtml(text.substring(idx, idx + query.length));
    var after = escapeHtml(text.substring(idx + query.length));
    return before + '<strong style="color:var(--secondary);">' + match + '</strong>' + after;
}

function escapeHtml(text) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

function selectStadium(stadiumId) {
    selectedStadiumId = stadiumId;
    sessionStorage.setItem('arenashield_stadium', stadiumId);

    fetch('/api/stadium/select', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stadium_id: stadiumId })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        const overlay = document.getElementById('stadiumSelector');
        if (overlay) overlay.style.display = 'none';

        initFanLayout(data);

        const nameEl = document.getElementById('currentStadiumName');
        if (nameEl && data.stadium) {
            nameEl.textContent = data.stadium.name;
        }

        const sidebarName = document.getElementById('sidebarStadiumName');
        if (sidebarName && data.stadium) {
            sidebarName.textContent = data.stadium.name;
        }

        const navInput = document.getElementById('navStadiumSearch');
        if (navInput && data.stadium) {
            navInput.placeholder = data.stadium.name;
        }

        if (data.stadium && data.stadium.gates && data.stadium.gates.length > 0) {
            const layoutInfo = document.getElementById('liveInfo');
            if (layoutInfo) {
                var extraHtml = '<div class="live-info-item" style="margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,0.1);">';
                extraHtml += '<span class="label">Gates: ' + data.stadium.gates.length + '</span>';
                extraHtml += '<span class="value">' + data.stadium.blocks.length + ' blocks</span>';
                extraHtml += '</div>';
                layoutInfo.insertAdjacentHTML('beforeend', extraHtml);
            }
        }
    })
    .catch(function() {
        initFanLayout();
    });
}

function initFanLayout(data) {
    const layout = document.getElementById('fanLayout');
    if (layout) layout.style.display = 'grid';

    if (data && data.stadium) {
        const navInput = document.getElementById('navStadiumSearch');
        if (navInput) navInput.placeholder = data.stadium.name;
    }

    loadLiveInfo();
}

function initStadiumChangeButton() {
    const btn = document.getElementById('changeStadiumBtn');
    const sidebarBtn = document.getElementById('changeStadiumSidebarBtn');
    const navSearch = document.getElementById('navbarSearch');
    var showSelector = function() {
        const overlay = document.getElementById('stadiumSelector');
        if (overlay) {
            overlay.style.display = 'flex';
            loadStadiums();
            setTimeout(function() {
                const input = document.getElementById('stadiumSearch');
                if (input) { input.value = ''; input.focus(); }
                const results = document.getElementById('searchResults');
                if (results) results.innerHTML = '<div class="search-hint"><i class="fas fa-globe"></i><span>774+ stadiums — search or click "Use default stadium" below</span></div>';
            }, 400);
        }
    };
    if (btn) btn.addEventListener('click', showSelector);
    if (sidebarBtn) sidebarBtn.addEventListener('click', showSelector);
    if (navSearch) navSearch.addEventListener('click', showSelector);

    var overlay = document.getElementById('stadiumSelector');
    if (overlay) {
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) overlay.style.display = 'none';
        });
    }

    var closeBtn = document.getElementById('closeStadiumSelector');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            if (overlay) overlay.style.display = 'none';
        });
    }
}

// ============================================
// CHAT FUNCTIONALITY
// ============================================

function initChat() {
    const form = document.getElementById('chatForm');
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const messages = document.getElementById('chatMessages');

    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = input.value.trim();
        if (!message) return;
        sendMessage(message);
        input.value = '';
    });

    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            form.dispatchEvent(new Event('submit'));
        }
    });

    const langSelect = document.getElementById('lang-select');
    if (langSelect) {
        let saved = sessionStorage.getItem('arenashield_lang');
        if (saved) langSelect.value = saved;
        langSelect.addEventListener('change', function() {
            sessionStorage.setItem('arenashield_lang', this.value);
        });
    }
}

function addMessage(content, role) {
    const messages = document.getElementById('chatMessages');
    if (!messages) return;

    const div = document.createElement('div');
    div.className = 'message ' + role;

    const icon = document.createElement('div');
    icon.className = 'message-icon';
    icon.innerHTML = role === 'assistant'
        ? '<i class="fas fa-robot"></i>'
        : '<i class="fas fa-user"></i>';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const formatted = formatMessage(content);
    contentDiv.innerHTML = formatted;

    div.appendChild(icon);
    div.appendChild(contentDiv);
    messages.appendChild(div);

    messages.scrollTop = messages.scrollHeight;
}

function formatMessage(text) {
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\n/g, '<br>');
    text = text.replace(/•/g, '&bull;');
    return text;
}

function showTypingIndicator() {
    const messages = document.getElementById('chatMessages');
    if (!messages) return null;

    const div = document.createElement('div');
    div.className = 'message assistant typing';
    div.id = 'typingIndicator';

    const icon = document.createElement('div');
    icon.className = 'message-icon';
    icon.innerHTML = '<i class="fas fa-robot"></i>';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Thinking...';

    div.appendChild(icon);
    div.appendChild(contentDiv);
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;

    return div;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

function sendMessage(message) {
    addMessage(message, 'user');
    const indicator = showTypingIndicator();

    const langSelect = document.getElementById('lang-select');
    const language = langSelect ? langSelect.value : 'en';

    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: message,
            session_id: sessionId,
            language: language,
            stadium_id: selectedStadiumId || sessionStorage.getItem('arenashield_stadium') || 'arenashield-national'
        })
    })
    .then(function(response) { return response.json(); })
    .then(function(data) {
        removeTypingIndicator();
        if (data.response) {
            addMessage(data.response, 'assistant');
        } else if (data.error) {
            addMessage('Error: ' + data.error, 'assistant');
        }
    })
    .catch(function(error) {
        removeTypingIndicator();
        addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
    });
}

function initQuickActions() {
    const buttons = document.querySelectorAll('.quick-btn');
    buttons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const msg = this.getAttribute('data-msg');
            const input = document.getElementById('chatInput');
            if (input) {
                input.value = msg;
                document.getElementById('chatForm').dispatchEvent(new Event('submit'));
            }
        });
    });
}

function initEmergencyButton() {
    const btn = document.getElementById('emergencyBtn');
    const modal = document.getElementById('emergencyModal');
    if (!btn || !modal) return;

    btn.addEventListener('click', function() {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    });

    modal.addEventListener('click', function(e) {
        if (e.target === modal) closeEmergencyModal();
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeEmergencyModal();
    });
}

function closeEmergencyModal() {
    const modal = document.getElementById('emergencyModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

// ============================================
// LIVE INFO SIDEBAR
// ============================================

function loadLiveInfo() {
    const container = document.getElementById('liveInfo');
    if (!container) return;

    fetch('/api/dashboard/overview')
    .then(function(r) { return r.json(); })
    .then(function(data) {
        let html = '';
        if (data.gates) {
            data.gates.forEach(function(gate) {
                html += '<div class="live-info-item">';
                html += '<span class="label"><span class="status-dot ' + gate.status + '"></span>' + gate.gate + '</span>';
                html += '<span class="value">' + gate.density + '%</span>';
                html += '</div>';
            });
        }
        html += '<div class="live-info-item">';
        html += '<span class="label">Total Visitors</span>';
        html += '<span class="value">' + (data.total_visitors || '--') + '</span>';
        html += '</div>';
        container.innerHTML = html;
    })
    .catch(function() {
        container.innerHTML = '<p style="color:var(--text-light);font-size:0.85rem;">Unable to load live data</p>';
    });
}

// ============================================
// DASHBOARD
// ============================================

function syncDashboardStadium() {
    var stored = sessionStorage.getItem('arenashield_stadium');
    var stadiumEl = document.getElementById('dashboardStadium');
    if (!stadiumEl) return;

    if (stored) {
        fetch('/api/stadium/select', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stadium_id: stored })
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.stadium && data.stadium.name) {
                stadiumEl.innerHTML = '<i class="fas fa-map-marker-alt"></i> <span>' + data.stadium.name + ', ' + data.stadium.location + '</span>';
            }
        }).catch(function() {
            stadiumEl.innerHTML = '<i class="fas fa-map-marker-alt"></i> <span>Default Stadium</span>';
        });
    } else {
        fetch('/api/dashboard/stadium')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.stadium && data.stadium.name) {
                stadiumEl.innerHTML = '<i class="fas fa-map-marker-alt"></i> <span>' + data.stadium.name + ', ' + data.stadium.location + '</span>';
            }
        }).catch(function() {});
    }
}

function initDashboard() {
    if (!document.querySelector('.dashboard-layout')) return;

    syncDashboardStadium();
    loadOverview();
    loadGates();
    loadAIAnalysis();
    loadIncidentCommander();
    loadAlerts();
    loadTransport();
    loadSustainability();

    if (autoRefresh) {
        refreshInterval = setInterval(refreshAll, 10000);
    }

    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            triggerRefresh();
        });
    }

    const autoBtn = document.getElementById('autoRefreshBtn');
    if (autoBtn) {
        autoBtn.addEventListener('click', function() {
            autoRefresh = !autoRefresh;
            this.classList.toggle('active');
            this.innerHTML = autoRefresh
                ? '<i class="fas fa-play"></i> Auto'
                : '<i class="fas fa-pause"></i> Manual';

            if (autoRefresh) {
                refreshInterval = setInterval(refreshAll, 10000);
            } else {
                clearInterval(refreshInterval);
            }
        });
    }

    const clearAlertsBtn = document.getElementById('clearAlertsBtn');
    if (clearAlertsBtn) {
        clearAlertsBtn.addEventListener('click', function() {
            fetch('/api/alerts/clear-all', { method: 'POST' })
            .then(function() { loadAlerts(); });
        });
    }
}

function refreshAll() {
    loadOverview();
    loadGates();
    loadAIAnalysis();
    loadIncidentCommander();
    loadAlerts();
    loadTransport();
    loadSustainability();
}

function triggerRefresh() {
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
        refreshBtn.disabled = true;
    }

    fetch('/api/dashboard/refresh', { method: 'POST' })
    .then(function(r) { return r.json(); })
    .then(function() {
        return fetch('/api/alerts/generate', { method: 'POST' });
    })
    .then(function() {
        refreshAll();
        loadLiveInfo();
    })
    .finally(function() {
        if (refreshBtn) {
            refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh Data';
            refreshBtn.disabled = false;
        }
    });
}

function loadOverview() {
    fetch('/api/dashboard/overview' + stadiumQueryParam())
    .then(function(r) { return r.json(); })
    .then(function(data) {
        setStat('totalVisitors', formatNumber(data.total_visitors));
        setStat('avgDensity', data.avg_density + '%');
        setStat('activeAlerts', data.active_alerts);
        setStat('medicalRequests', data.medical_requests);
        setStat('shuttleBuses', data.shuttle_buses ? data.shuttle_buses.operational || '--' : '--');
        setStat('securityAlerts', data.security_alerts || 0);
        if (data.stadium && data.stadium.name) {
            var el = document.getElementById('dashboardStadium');
            if (el) el.innerHTML = '<i class="fas fa-map-marker-alt"></i> <span>' + data.stadium.name + ', ' + data.stadium.location + '</span>';
        }
    });
}

function stadiumQueryParam() {
    var stored = sessionStorage.getItem('arenashield_stadium');
    if (stored) {
        return '?stadium_id=' + encodeURIComponent(stored);
    }
    return '';
}

function setStat(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

function formatNumber(num) {
    if (!num && num !== 0) return '--';
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function loadGates() {
    const grid = document.getElementById('gateGrid');
    if (!grid) return;

    fetch('/api/dashboard/gates' + stadiumQueryParam())
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (!data.gates || data.gates.length === 0) {
            grid.innerHTML = '<p style="padding:1rem;color:var(--text-light);">No gate data available</p>';
            return;
        }

        let html = '';
        data.gates.forEach(function(gate) {
            var statusClass = gate.status || 'normal';
            html += '<div class="gate-card ' + statusClass + '">';
            html += '<div class="gate-header">';
            html += '<span class="gate-name">Gate ' + gate.gate + '</span>';
            html += '<span class="gate-status ' + statusClass + '">' + statusClass + '</span>';
            html += '</div>';
            html += '<div class="gate-details">';
            html += '<div class="gate-detail-item"><span class="label">Density</span><span class="value">' + gate.density + '%</span></div>';
            html += '<div class="gate-detail-item"><span class="label">Queue</span><span class="value">' + gate.queue_time + ' min</span></div>';
            html += '<div class="gate-detail-item"><span class="label">Flow</span><span class="value">' + gate.crowd_flow + '</span></div>';
            html += '</div>';
            html += '<div class="density-bar"><div class="density-bar-fill" style="width:' + gate.density + '%;background:' + getDensityColor(gate.density) + ';"></div></div>';
            html += '</div>';
        });
        grid.innerHTML = html;
    })
    .catch(function() {
        grid.innerHTML = '<p style="padding:1rem;color:var(--text-light);">Failed to load gate data</p>';
    });
}

function getDensityColor(density) {
    if (density >= 80) return '#C62828';
    if (density >= 50) return '#F57C00';
    return '#2E7D32';
}

function loadAIAnalysis() {
    const container = document.getElementById('aiCopilotContent');
    if (!container) return;

    fetch('/api/dashboard/ai-analysis' + stadiumQueryParam())
    .then(function(r) { return r.json(); })
    .then(function(data) {
        var riskLevel = data.risk_level || 'low';
        var riskIcon = riskLevel === 'high' ? '&#9888;&#65039;' : (riskLevel === 'medium' ? '&#9888;' : '&#9989;');

        var html = '';
        html += '<div class="ai-risk ' + riskLevel + '">' + riskIcon + ' Risk Level: ' + riskLevel.toUpperCase() + '</div>';

        if (data.summary) {
            html += '<div class="ai-summary">' + data.summary + '</div>';
        }

        if (data.recommendations && data.recommendations.length > 0) {
            html += '<h4 style="font-size:0.85rem;margin-bottom:0.5rem;">AI Recommendations:</h4>';
            html += '<ul class="ai-recommendations">';
            data.recommendations.forEach(function(rec) {
                html += '<li>' + rec + '</li>';
            });
            html += '</ul>';
        }

        container.innerHTML = html;
    })
    .catch(function() {
        container.innerHTML = '<p style="padding:1rem;color:var(--text-light);">AI analysis unavailable</p>';
    });
}

function loadIncidentCommander() {
    const container = document.getElementById('incidentCommanderContent');
    const badge = document.getElementById('incidentBadge');
    if (!container) return;

    fetch('/api/dashboard/incident-commander' + stadiumQueryParam())
    .then(function(r) { return r.json(); })
    .then(function(data) {
        var priority = data.priority || 'LOW';

        if (badge) {
            badge.textContent = priority;
            badge.style.background = priority === 'CRITICAL' ? '#C62828' : priority === 'HIGH' ? '#F57C00' : '#2E7D32';
            badge.style.color = '#FFFFFF';
            badge.style.fontWeight = '600';
        }

        var html = '';
        html += '<div class="ai-risk ' + priority.toLowerCase() + '">&#9878; Priority: ' + priority + '</div>';

        if (data.situation) {
            html += '<div class="ai-summary">' + data.situation + '</div>';
        }

        if (data.ai_commands) {
            if (typeof data.ai_commands === 'string') {
                html += '<div class="ai-summary" style="margin-top:8px;">' + formatMessage(data.ai_commands) + '</div>';
            } else if (Array.isArray(data.ai_commands)) {
                html += '<h4 style="font-size:0.85rem;margin-bottom:0.5rem;">Commands:</h4>';
                html += '<ul class="ai-recommendations">';
                data.ai_commands.forEach(function(cmd) {
                    html += '<li>' + cmd + '</li>';
                });
                html += '</ul>';
            }
        }

        container.innerHTML = html;
    })
    .catch(function() {
        container.innerHTML = '<p style="padding:1rem;color:var(--text-light);">Incident Commander unavailable</p>';
    });
}

function loadSustainability() {
    const container = document.getElementById('sustainabilityContent');
    if (!container) return;

    fetch('/api/dashboard/sustainability')
    .then(function(r) { return r.json(); })
    .then(function(data) {
        var html = '';
        html += '<div class="transport-grid">';
        html += '<div class="transport-item"><div class="label">Energy</div><div class="value">' + data.energy_optimization + '% optimized</div></div>';
        html += '<div class="transport-item"><div class="label">Water</div><div class="value">' + data.water_consumption + '% efficiency</div></div>';
        html += '<div class="transport-item"><div class="label">Carbon</div><div class="value" style="text-transform:capitalize;">' + data.carbon_footprint + '</div></div>';
        html += '</div>';

        if (data.waste_bins) {
            html += '<h4 style="font-size:0.75rem;margin:8px 0 4px;color:var(--text-light);">Waste Bins:</h4>';
            data.waste_bins.forEach(function(bin) {
                var statusClass = bin.fill_level > 80 ? 'full' : 'available';
                html += '<div style="display:flex;justify-content:space-between;padding:2px 0;font-size:0.75rem;">';
                html += '<span>Gate ' + bin.gate + '</span>';
                html += '<span>' + bin.fill_level + '% <span class="parking-status ' + statusClass + '">' + bin.status + '</span></span>';
                html += '</div>';
            });
        }

        if (data.ai_suggestion) {
            html += '<div style="margin-top:8px;padding:6px;background:rgba(212,175,55,0.1);border-radius:6px;font-size:0.75rem;">';
            html += '<i class="fas fa-lightbulb" style="color:var(--accent);"></i> ' + data.ai_suggestion;
            html += '</div>';
        }

        container.innerHTML = html;
    })
    .catch(function() {
        container.innerHTML = '<p style="padding:1rem;color:var(--text-light);">Sustainability data unavailable</p>';
    });
}

function loadAlerts() {
    const list = document.getElementById('alertsList');
    if (!list) return;

    fetch('/api/alerts')
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (!data || data.length === 0) {
            list.innerHTML = '<div class="no-alerts"><i class="fas fa-check-circle"></i> All clear! No active alerts.</div>';
            return;
        }

        var html = '';
        data.forEach(function(alert) {
            var severity = alert.severity || 'info';
            html += '<div class="alert-item ' + severity + '">';
            html += '<div class="alert-info">';
            html += '<div class="alert-gate">' + alert.gate + ' - ' + alert.alert_type.replace(/_/g, ' ') + '</div>';
            html += '<div class="alert-message">' + alert.message + '</div>';
            html += '</div></div>';
        });
        list.innerHTML = html;
    })
    .catch(function() {
        list.innerHTML = '<p style="padding:1rem;color:var(--text-light);">Failed to load alerts</p>';
    });
}

function loadTransport() {
    const container = document.getElementById('transportInfo');
    if (!container) return;

    fetch('/api/dashboard/overview')
    .then(function(r) { return r.json(); })
    .then(function(data) {
        var shuttle = data.shuttle_buses || {};
        var parking = data.parking || {};

        var html = '<div class="transport-grid">';
        html += '<div class="transport-item"><div class="label">Buses Active</div><div class="value">' + (shuttle.operational || 0) + '</div></div>';
        html += '<div class="transport-item"><div class="label">En Route</div><div class="value">' + (shuttle.en_route || 0) + '</div></div>';

        for (var lot in parking) {
            var p = parking[lot];
            html += '<div class="transport-item">';
            html += '<div class="label">' + lot.replace(/_/g, ' ').toUpperCase() + '</div>';
            html += '<div class="value">' + p.filled + '/' + p.capacity + ' <span class="parking-status ' + (p.status || 'available') + '">' + (p.status || 'available') + '</span></div>';
            html += '</div>';
        }

        html += '</div>';
        container.innerHTML = html;
    })
    .catch(function() {
        container.innerHTML = '<p style="padding:1rem;color:var(--text-light);">Transport data unavailable</p>';
    });
}
