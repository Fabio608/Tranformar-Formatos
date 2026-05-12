<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prode Mundial 2026 - Grupos de Amigos</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;700&display=swap');
        
        body { 
            font-family: 'Inter', sans-serif; 
            background: linear-gradient(180deg, #74ACDF 0%, #FFFFFF 50%, #74ACDF 100%);
            background-attachment: fixed;
        }
        .bebas { font-family: 'Bebas Neue', cursive; }
        
        .fifa-gradient {
            background: linear-gradient(135deg, #003566 0%, #001d3d 100%);
        }
        .card { 
            background: white; 
            border-radius: 1rem; 
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); 
            transition: transform 0.2s;
        }
        .card:hover { transform: translateY(-2px); }
        .tab-active { border-bottom: 4px solid #F6B40E; color: #003566; font-weight: bold; }
        
        /* Animaciones */
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .animate-fade { animation: fadeIn 0.5s ease-in; }
    </style>
</head>
<body class="min-h-screen pb-20">

    <!-- Header -->
    <header class="fifa-gradient text-white p-6 shadow-xl sticky top-0 z-50">
        <div class="max-w-4xl mx-auto flex justify-between items-center">
            <h1 class="bebas text-3xl tracking-wider">⚽ MUNDIAL 2026 PRODE</h1>
            <div id="userBadge" class="hidden flex items-center bg-blue-900 rounded-full px-4 py-1">
                <span id="userNameDisplay" class="text-sm font-bold">Invitado</span>
            </div>
        </div>
    </header>

    <!-- App Container -->
    <main class="max-w-4xl mx-auto p-4 animate-fade">
        
        <!-- Auth / Welcome Section -->
        <div id="authSection" class="card p-8 text-center my-8">
            <h2 class="bebas text-4xl text-blue-900 mb-4 italic">Bienvenido al Prode Mundial 2026</h2>
            <p class="text-gray-600 mb-6">Crea un grupo con tus amigos, carga tus predicciones y mira quién sabe más de fútbol.</p>
            <input type="text" id="userNameInput" placeholder="Tu Nombre o Apodo" class="w-full max-w-xs border-2 border-gray-200 rounded-lg p-3 mb-4 text-center focus:border-blue-500 outline-none">
            <button onclick="login()" class="bg-yellow-500 hover:bg-yellow-600 text-blue-900 font-bold py-3 px-8 rounded-lg shadow-lg transition w-full max-w-xs">
                INGRESAR
            </button>
        </div>

        <!-- Main Dashboard (Hidden initially) -->
        <div id="mainDashboard" class="hidden">
            
            <!-- Navigation Tabs -->
            <div class="flex justify-around bg-white rounded-t-xl border-b overflow-x-auto">
                <button onclick="showTab('tab-groups')" id="btn-tab-groups" class="p-4 flex-1 tab-active">GRUPOS</button>
                <button onclick="showTab('tab-predict')" id="btn-tab-predict" class="p-4 flex-1">MI PRODE</button>
                <button onclick="showTab('tab-ranking')" id="btn-tab-ranking" class="p-4 flex-1">RANKING</button>
                <button onclick="showTab('tab-real')" id="btn-tab-real" class="p-4 flex-1 text-xs text-red-600 uppercase">Admin Resultados</button>
            </div>

            <!-- Tab: Groups -->
            <div id="tab-groups" class="tab-content card rounded-t-none p-6 space-y-6">
                <div class="grid md:grid-cols-2 gap-4">
                    <div class="border-r md:pr-4">
                        <h3 class="bebas text-2xl text-blue-900 mb-2">Crear Nuevo Grupo</h3>
                        <input type="text" id="newGroupName" placeholder="Nombre del Grupo" class="w-full border p-2 rounded mb-2">
                        <button onclick="createGroup()" class="bg-blue-900 text-white w-full py-2 rounded font-bold hover:bg-blue-800">CREAR</button>
                    </div>
                    <div>
                        <h3 class="bebas text-2xl text-blue-900 mb-2">Unirse a Grupo</h3>
                        <input type="text" id="joinGroupCode" placeholder="Código de Grupo" class="w-full border p-2 rounded mb-2">
                        <button onclick="joinGroup()" class="bg-green-600 text-white w-full py-2 rounded font-bold hover:bg-green-700">UNIRSE</button>
                    </div>
                </div>
                
                <div id="activeGroupInfo" class="hidden bg-yellow-50 p-4 border-2 border-yellow-200 rounded-xl">
                    <p class="text-sm text-yellow-800 font-bold uppercase">Grupo Actual:</p>
                    <div class="flex justify-between items-center">
                        <h4 id="currentGroupName" class="bebas text-3xl text-blue-900">---</h4>
                        <div class="text-right">
                            <span class="text-xs text-gray-500">CÓDIGO:</span>
                            <p id="currentGroupCode" class="font-mono font-bold text-xl select-all">---</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab: Predictions -->
            <div id="tab-predict" class="tab-content hidden card rounded-t-none p-6">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="bebas text-2xl text-blue-900">Mis Predicciones</h3>
                    <button onclick="savePredictions()" class="bg-yellow-500 text-blue-900 px-4 py-1 rounded-full font-bold text-sm shadow">GUARDAR TODO</button>
                </div>
                <div id="groupsContainer" class="space-y-4 max-h-[60vh] overflow-y-auto pr-2">
                    <!-- Los grupos se cargan aquí dinámicamente -->
                </div>
            </div>

            <!-- Tab: Ranking -->
            <div id="tab-ranking" class="tab-content hidden card rounded-t-none p-6">
                <h3 class="bebas text-2xl text-blue-900 mb-4">Tabla de Amigos</h3>
                <div id="rankingList" class="space-y-2">
                    <p class="text-center text-gray-400 italic">Selecciona un grupo para ver el ranking...</p>
                </div>
                <div class="mt-6 p-4 bg-blue-50 rounded-lg text-xs text-blue-800">
                    <p><b>Puntaje:</b> 3 pts por ganador/empate acertado. 0 pts si fallas.</p>
                    <p class="mt-1 italic">En caso de empate, se recomienda seguir el criterio oficial de la FIFA (Golaverage, Fair Play) mediante el link oficial.</p>
                    <a href="https://www.fifa.com/fifaplus/es/tournaments/mens/worldcup/canadamexicousa2026" target="_blank" class="text-blue-600 underline block mt-2">Ver Reglamento FIFA 2026</a>
                </div>
            </div>

            <!-- Tab: Real Results (Simulator of official results) -->
            <div id="tab-real" class="tab-content hidden card rounded-t-none p-6">
                <div class="bg-red-50 border border-red-200 p-4 rounded-lg mb-4">
                    <h4 class="text-red-700 font-bold mb-1 underline">MODO ADMIN (Simulación)</h4>
                    <p class="text-xs text-red-600">En una app real, estos datos vendrían de una API oficial. Aquí puedes poner los resultados reales para ver cómo cambia el ranking.</p>
                </div>
                <div id="realResultsContainer" class="space-y-4"></div>
                <button onclick="saveRealResults()" class="mt-4 bg-red-600 text-white w-full py-2 rounded-lg font-bold">ACTUALIZAR RESULTADOS OFICIALES</button>
            </div>

        </div>
    </main>

    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore, doc, getDoc, setDoc, updateDoc, onSnapshot, collection, query, where, addDoc, getDocs } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

        // Configuración
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'mundial-prode-2026';
        const firebaseConfig = JSON.parse(__firebase_config);
        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);
        const auth = getAuth(app);

        // Estado Global
        let currentUser = null;
        let currentGroupId = localStorage.getItem('prode_group_id');
        let myPredictions = {};
        let realResults = {};

        const ZONAS = {
            "A": ["México", "Sudáfrica", "Corea del Sur", "R. Checa"],
            "B": ["Canadá", "Bosnia", "Qatar", "Suiza"],
            "C": ["Brasil", "Marruecos", "Haití", "Escocia"],
            "D": ["EE.UU.", "Australia", "Paraguay", "Turquía"],
            "E": ["Alemania", "Curazao", "C. de Marfil", "Ecuador"],
            "F": ["Paises Bajos", "Japón", "Suecia", "Tunez"],
            "G": ["Belgica", "Egipto", "Irán", "N. Zelanda"],
            "H": ["España", "Cabo Verde", "A. Saudita", "Uruguay"],
            "I": ["Francia", "Senegal", "Irak", "Noruega"],
            "J": ["Argentina", "Argelia", "Jordania", "Austria"],
            "K": ["Portugal", "RD Congo", "Uzbequistan", "Colombia"],
            "L": ["Inglaterra", "Croacia", "Ghana", "Panamá"]
        };

        window.login = async () => {
            const name = document.getElementById('userNameInput').value.trim();
            if (!name) return alert("Por favor ingresa tu nombre");
            
            try {
                const userCredential = await signInAnonymously(auth);
                currentUser = userCredential.user;
                
                // Guardar perfil de usuario
                const userRef = doc(db, 'artifacts', appId, 'users', currentUser.uid, 'profile');
                await setDoc(userRef, { name, uid: currentUser.uid });

                document.getElementById('authSection').classList.add('hidden');
                document.getElementById('mainDashboard').classList.remove('hidden');
                document.getElementById('userBadge').classList.remove('hidden');
                document.getElementById('userNameDisplay').innerText = name;

                initApp();
            } catch (error) {
                console.error("Error login:", error);
            }
        };

        async function initApp() {
            // Cargar Mis Predicciones iniciales
            const predRef = doc(db, 'artifacts', appId, 'users', currentUser.uid, 'prode', 'predictions');
            const predSnap = await getDoc(predRef);
            if (predSnap.exists()) myPredictions = predSnap.data();

            // Suscribirse a Resultados Reales (Público)
            const realRef = doc(db, 'artifacts', appId, 'public', 'data', 'realResults');
            onSnapshot(realRef, (snap) => {
                if (snap.exists()) {
                    realResults = snap.data();
                    renderAll();
                }
            }, (err) => console.log("Real results monitor error", err));

            renderAll();
            if (currentGroupId) refreshGroupInfo();
        }

        window.showTab = (tabId) => {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.add('hidden'));
            document.querySelectorAll('[id^="btn-tab-"]').forEach(b => b.classList.remove('tab-active'));
            document.getElementById(tabId).classList.remove('hidden');
            document.getElementById('btn-' + tabId).classList.add('tab-active');
            
            if (tabId === 'tab-ranking') loadRanking();
        };

        window.createGroup = async () => {
            const name = document.getElementById('newGroupName').value.trim();
            if (!name) return;
            const code = Math.random().toString(36).substring(2, 8).toUpperCase();
            
            const groupRef = await addDoc(collection(db, 'artifacts', appId, 'public', 'data', 'groups'), {
                name,
                code,
                owner: currentUser.uid,
                createdAt: new Date().toISOString()
            });
            
            currentGroupId = groupRef.id;
            localStorage.setItem('prode_group_id', currentGroupId);
            refreshGroupInfo();
            alert("Grupo creado con éxito!");
        };

        window.joinGroup = async () => {
            const code = document.getElementById('joinGroupCode').value.trim().toUpperCase();
            const q = query(collection(db, 'artifacts', appId, 'public', 'data', 'groups'));
            const querySnapshot = await getDocs(q);
            
            let found = false;
            querySnapshot.forEach((doc) => {
                if (doc.data().code === code) {
                    currentGroupId = doc.id;
                    found = true;
                }
            });

            if (found) {
                localStorage.setItem('prode_group_id', currentGroupId);
                refreshGroupInfo();
                alert("¡Te has unido al grupo!");
                showTab('tab-groups');
            } else {
                alert("Código de grupo no encontrado.");
            }
        };

        async function refreshGroupInfo() {
            const gRef = doc(db, 'artifacts', appId, 'public', 'data', 'groups', currentGroupId);
            const gSnap = await getDoc(gRef);
            if (gSnap.exists()) {
                const data = gSnap.data();
                document.getElementById('activeGroupInfo').classList.remove('hidden');
                document.getElementById('currentGroupName').innerText = data.name;
                document.getElementById('currentGroupCode').innerText = data.code;
                
                // Unir al usuario al grupo (en su perfil para el ranking)
                const userRef = doc(db, 'artifacts', appId, 'users', currentUser.uid, 'profile');
                await updateDoc(userRef, { currentGroup: currentGroupId });
            }
        }

        function renderAll() {
            const containers = ['groupsContainer', 'realResultsContainer'];
            containers.forEach(id => {
                const isReal = id === 'realResultsContainer';
                const source = isReal ? realResults : myPredictions;
                let html = "";
                
                for (const [z, teams] of Object.entries(ZONAS)) {
                    html += `<div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                        <p class="font-bold text-blue-900 mb-2 border-b">ZONA ${z}</p>`;
                    
                    for (let i = 0; i < teams.length; i++) {
                        for (let j = i + 1; j < teams.length; j++) {
                            const key = `${z}_${teams[i]}_${teams[j]}`;
                            const val = source[key] || "Pendiente";
                            html += `
                            <div class="flex items-center justify-between py-1 text-sm">
                                <span class="w-1/3 text-right pr-2">${teams[i]}</span>
                                <select onchange="updateMatch('${id}', '${key}', this.value)" 
                                    class="w-1/3 text-xs p-1 border rounded ${val === 'Pendiente' ? 'bg-white' : 'bg-blue-100 font-bold'}">
                                    <option ${val === 'Pendiente' ? 'selected' : ''}>Pendiente</option>
                                    <option value="Gana ${teams[i]}" ${val === 'Gana ' + teams[i] ? 'selected' : ''}>Gana ${teams[i]}</option>
                                    <option value="Gana ${teams[j]}" ${val === 'Gana ' + teams[j] ? 'selected' : ''}>Gana ${teams[j]}</option>
                                    <option value="Empate" ${val === 'Empate' ? 'selected' : ''}>Empate</option>
                                </select>
                                <span class="w-1/3 text-left pl-2">${teams[j]}</span>
                            </div>`;
                        }
                    }
                    html += `</div>`;
                }
                document.getElementById(id).innerHTML = html;
            });
        }

        window.updateMatch = (container, key, value) => {
            if (container === 'realResultsContainer') {
                realResults[key] = value;
            } else {
                myPredictions[key] = value;
            }
        };

        window.savePredictions = async () => {
            const predRef = doc(db, 'artifacts', appId, 'users', currentUser.uid, 'prode', 'predictions');
            await setDoc(predRef, myPredictions);
            // También guardamos una copia pública para que otros amigos puedan verla en el ranking
            const publicRef = doc(db, 'artifacts', appId, 'public', 'data', 'shared_predictions', currentUser.uid);
            await setDoc(publicRef, { 
                predictions: myPredictions, 
                userId: currentUser.uid, 
                userName: document.getElementById('userNameDisplay').innerText,
                groupId: currentGroupId 
            });
            alert("¡Predicciones guardadas!");
        };

        window.saveRealResults = async () => {
            const realRef = doc(db, 'artifacts', appId, 'public', 'data', 'realResults');
            await setDoc(realRef, realResults);
            alert("¡Resultados oficiales actualizados!");
        };

        async function loadRanking() {
            if (!currentGroupId) return;
            const rankingDiv = document.getElementById('rankingList');
            rankingDiv.innerHTML = "<p class='text-center'>Calculando puntos...</p>";
            
            // Buscamos todas las predicciones que tengan este groupId
            const q = query(collection(db, 'artifacts', appId, 'public', 'data', 'shared_predictions'), 
                           where("groupId", "==", currentGroupId));
            const querySnapshot = await getDocs(q);
            
            let usersScores = [];

            querySnapshot.forEach((docSnap) => {
                const data = docSnap.data();
                let score = 0;
                
                // Comparar predicción vs resultados reales
                for (const [matchKey, predVal] of Object.entries(data.predictions)) {
                    if (predVal !== "Pendiente" && realResults[matchKey] === predVal) {
                        score += 3; // 3 puntos por acierto
                    }
                }
                
                usersScores.push({ name: data.userName, score: score, isMe: data.userId === currentUser.uid });
            });

            // Ordenar por score descendente
            usersScores.sort((a, b) => b.score - a.score);

            if (usersScores.length === 0) {
                rankingDiv.innerHTML = "<p class='text-center text-gray-400'>Nadie en este grupo ha guardado predicciones aún.</p>";
                return;
            }

            let html = "";
            usersScores.forEach((u, i) => {
                html += `
                <div class="flex items-center justify-between p-3 rounded-lg ${u.isMe ? 'bg-yellow-100 border-2 border-yellow-400' : 'bg-white border'}">
                    <div class="flex items-center gap-3">
                        <span class="bebas text-xl text-gray-400">${i+1}°</span>
                        <span class="font-bold text-blue-900">${u.name} ${u.isMe ? '(Tú)' : ''}</span>
                    </div>
                    <span class="bebas text-2xl text-yellow-600">${u.score} <small class="text-xs">PTS</small></span>
                </div>`;
            });
            rankingDiv.innerHTML = html;
        }

    </script>
</body>
</html>
