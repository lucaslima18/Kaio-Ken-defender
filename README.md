# Kaio-Ken-defender
an project who connects you enterprise project with security



![kaio_ken_defender_icon](https://github.com/user-attachments/assets/7d350ebb-ed75-4cbc-b914-6babefab23af)
<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Gradiente laranja das esferas -->
    <radialGradient id="orbGrad" cx="50%" cy="40%">
      <stop offset="0%" style="stop-color:#fbbf24;stop-opacity:1" />
      <stop offset="70%" style="stop-color:#f59e0b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#d97706;stop-opacity:1" />
    </radialGradient>
  </defs>

  <!-- Aura Kaio-Ken pulsante em camadas -->
  <ellipse cx="100" cy="100" rx="90" ry="95" fill="url(#redAura)" opacity="0.5">
    <animate attributeName="rx" values="90;95;90" dur="1.5s" repeatCount="indefinite"/>
    <animate attributeName="ry" values="95;100;95" dur="1.5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.5;0.3;0.5" dur="1.5s" repeatCount="indefinite"/>
  </ellipse>
  
  <ellipse cx="100" cy="100" rx="80" ry="85" fill="url(#redAura)" opacity="0.6">
    <animate attributeName="rx" values="80;85;80" dur="1.2s" repeatCount="indefinite"/>
    <animate attributeName="ry" values="85;90;85" dur="1.2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.6;0.4;0.6" dur="1.2s" repeatCount="indefinite"/>
  </ellipse>

  <ellipse cx="100" cy="100" rx="70" ry="75" fill="url(#redAura)" opacity="0.4">
    <animate attributeName="rx" values="70;75;70" dur="1s" repeatCount="indefinite"/>
    <animate attributeName="ry" values="75;80;75" dur="1s" repeatCount="indefinite"/>
  </ellipse>

  <!-- Escudo principal -->
  <path d="M 100 20 L 160 50 L 160 115 Q 160 160 100 185 Q 40 160 40 115 L 40 50 Z" 
        fill="url(#shieldGrad)" 
        stroke="#3b82f6" 
        stroke-width="3"
        filter="url(#glow)"/>
  
  <!-- Borda interna do escudo (detalhes) -->
  <path d="M 100 30 L 150 55 L 150 112 Q 150 150 100 172 Q 50 150 50 112 L 50 55 Z" 
        fill="none" 
        stroke="#60a5fa" 
        stroke-width="1.5"
        opacity="0.4"/>

  <!-- Detalhes laterais do escudo -->
  <path d="M 50 55 L 50 112" stroke="#1e3a8a" stroke-width="2" opacity="0.5"/>
  <path d="M 150 55 L 150 112" stroke="#1e3a8a" stroke-width="2" opacity="0.5"/>

  <!-- Esfera do Dragão dentro do escudo -->
  <circle cx="100" cy="100" r="45" fill="url(#orbGrad)" filter="url(#glow)"/>
  
  <!-- Brilho superior da esfera -->
  <ellipse cx="92" cy="88" rx="18" ry="13" fill="#fef3c7" opacity="0.7"/>
  
  <!-- Sombra interna da esfera -->
  <circle cx="100" cy="100" r="45" fill="none" stroke="#b45309" stroke-width="2" opacity="0.3"/>

  <!-- Configuração de 4 estrelas -->
  <g id="stars">
    <!-- Estrela superior esquerda -->
    <g transform="translate(85, 85)">
      <path d="M 0,-7 L 1.8,-1.8 L 7,-1.8 L 2.5,1.8 L 4.3,7 L 0,3.5 L -4.3,7 L -2.5,1.8 L -7,-1.8 L -1.8,-1.8 Z" 
            fill="url(#starGrad)" 
            stroke="#450a0a" 
            stroke-width="0.5"/>
    </g>
  </g>
  <g opacity="0.8">
    <circle cx="30" cy="60" r="2.5" fill="#ff0000">
      <animate attributeName="cy" values="60;40;60" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="170" cy="80" r="3" fill="#dc2626">
      <animate attributeName="cy" values="80;60;80" dur="2.5s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0.2;1" dur="2.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="25" cy="120" r="2" fill="#ef4444">
      <animate attributeName="cy" values="120;100;120" dur="1.8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0.4;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <circle cx="175" cy="130" r="2.5" fill="#ff0000">
      <animate attributeName="cy" values="130;150;130" dur="2.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0.3;1" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="45" cy="165" r="2" fill="#dc2626">
      <animate attributeName="cx" values="45;35;45" dur="1.5s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="155" cy="35" r="3" fill="#ef4444">
      <animate attributeName="cx" values="155;165;155" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
    </circle>
  </g>

  <g opacity="0.5">
    <line x1="100" y1="100" x2="100" y2="15" stroke="#ff0000" stroke-width="2">
      <animate attributeName="opacity" values="0.5;0.1;0.5" dur="1s" repeatCount="indefinite"/>
    </line>
    <line x1="100" y1="100" x2="165" y2="45" stroke="#dc2626" stroke-width="1.5">
      <animate attributeName="opacity" values="0.4;0.1;0.4" dur="1.3s" repeatCount="indefinite"/>
    </line>
    <line x1="100" y1="100" x2="35" y2="45" stroke="#ef4444" stroke-width="1.5">
      <animate attributeName="opacity" values="0.3;0.1;0.3" dur="1.6s" repeatCount="indefinite"/>
    </line>
    <line x1="100" y1="100" x2="165" y2="155" stroke="#ff0000" stroke-width="1.5">
      <animate attributeName="opacity" values="0.4;0.1;0.4" dur="1.4s" repeatCount="indefinite"/>
    </line>
    <line x1="100" y1="100" x2="35" y2="155" stroke="#dc2626" stroke-width="1.5">
      <animate attributeName="opacity" values="0.3;0.1;0.3" dur="1.7s" repeatCount="indefinite"/>
    </line>
  </g>
</svg>
