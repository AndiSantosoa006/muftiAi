<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Syamilah AI Assistant</title>
    {{-- FOUC Prevention: apply dark mode before React loads --}}
    <script>
        (function() {
            var t = localStorage.getItem('mufti-theme');
            if (t === 'dark' || (!t && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.classList.add('dark');
            }
        })();
    </script>
    @viteReactRefresh
    @vite('resources/js/app.jsx')
</head>
<body class="bg-gray-50 dark:bg-slate-950 m-0 p-0 transition-colors duration-300">
    <div id="root"></div>

    @viteReactRefresh
    @vite('resources/js/app.jsx')
</body>
</html>
