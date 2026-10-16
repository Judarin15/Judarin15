# Perfil de GitHub RINCÓN/OS

Este repositorio pinta tu perfil de GitHub con la estética de tu portafolio.

## 1. Subirlo (una sola vez)

1. En GitHub crea un repositorio **público** llamado exactamente `Judarin15`
   (igual que tu usuario). GitHub mostrará el aviso de que es un repositorio especial.
   No marques "Add a README".
2. Desde esta carpeta:
   ```
   git init
   git add .
   git commit -m "Perfil RINCÓN/OS"
   git branch -M main
   git remote add origin https://github.com/Judarin15/Judarin15.git
   git push -u origin main
   ```
3. En el repositorio: **Settings > Actions > General > Workflow permissions**, marca
   **Read and write permissions** y guarda.
4. Pestaña **Actions > RINCÓN/OS > Run workflow**. En un minuto aparecen tus estadísticas
   reales y la serpiente. Desde ahí se actualiza sola todos los días.

## 2. Ajustes del perfil (Edit profile)

- **Name:** Julián Rincón
- **Bio:** Desarrollador web junior en Cúcuta. Tecnólogo SENA en ADSO y estudiante de Ing. de Sistemas.
- **Location:** Cúcuta, Colombia
- **Website:** https://portafolio-de-proyectos-julian.web.app/
- Marca **Available for hire** si te aparece la opción.
- En **Settings > Public profile > Contributions & activity** activa
  **Include private contributions on my profile** para que tus aportes privados cuenten.

## 3. Repositorios fijados (Customize your pins)

Fija estos, en este orden: **Intranet**, **TechMarket**, **Portafolio**, **CV**,
**ProyectoSpring**, **PhpSena**. Ponle descripción a cada uno (engranaje junto a "About"):

- Intranet: Intranet institucional del Gimnasio Campestre Comfaoriente. React, TypeScript, Firebase.
- TechMarket: Tienda en línea de electrónica y gaming. React, Vite y Supabase.
- Portafolio: Mi portafolio como terminal CRT animada.

## 4. Cambiar el contenido

Los datos están al inicio de `scripts/generar_svgs.py` (perfil, proyectos, habilidades,
trayectoria). Edítalos y ejecuta:

```
pip install fonttools brotli
python scripts/generar_svgs.py
```

Luego haz commit y push. Las estadísticas (`assets/estadisticas.svg`) y la serpiente
(`assets/serpiente.svg`) las genera la acción; no las edites a mano.

## Archivos

| Archivo | Qué es |
| --- | --- |
| `README.md` | Lo que se ve en tu perfil. |
| `assets/*.svg` | Paneles animados, con las fuentes incrustadas. |
| `scripts/generar_svgs.py` | Genera los paneles a partir de tus datos. |
| `scripts/stats.mjs` | Dibuja tus estadísticas reales con la API de GitHub. |
| `.github/workflows/rincon-os.yml` | Acción diaria: estadísticas y serpiente. |
| `scripts/fonts/` | VT323 e IBM Plex Mono (licencia OFL incluida). |
