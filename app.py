from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GitOps Pipeline</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }

            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
            }

            .container {
                text-align: center;
                padding: 60px 40px;
                background: rgba(255,255,255,0.05);
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                box-shadow: 0 0 40px rgba(100, 100, 255, 0.3);
                max-width: 700px;
                width: 90%;
            }

            .badge {
                display: inline-block;
                background: linear-gradient(90deg, #00c9ff, #92fe9d);
                color: #000;
                font-weight: bold;
                font-size: 0.8rem;
                padding: 5px 15px;
                border-radius: 20px;
                margin-bottom: 20px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }

            h1 {
                font-size: 3rem;
                font-weight: 800;
                background: linear-gradient(90deg, #00c9ff, #92fe9d, #f7971e);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 15px;
            }

            p {
                font-size: 1.1rem;
                color: rgba(255,255,255,0.6);
                margin-bottom: 30px;
            }

            .stack {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 10px;
                margin-bottom: 30px;
            }

            .tag {
                padding: 8px 18px;
                border-radius: 30px;
                font-size: 0.85rem;
                font-weight: 600;
                letter-spacing: 1px;
            }

            .tag-blue  { background: rgba(0, 150, 255, 0.2); border: 1px solid #0096ff; color: #0096ff; }
            .tag-green { background: rgba(0, 255, 150, 0.2); border: 1px solid #00ff96; color: #00ff96; }
            .tag-orange{ background: rgba(255, 150, 0, 0.2); border: 1px solid #ff9600; color: #ff9600; }
            .tag-pink  { background: rgba(255, 0, 150, 0.2); border: 1px solid #ff0096; color: #ff0096; }
            .tag-purple{ background: rgba(150, 0, 255, 0.2); border: 1px solid #9600ff; color: #9600ff; }

            .version {
                font-size: 0.85rem;
                color: rgba(255,255,255,0.3);
                margin-top: 20px;
            }

            .pulse {
                display: inline-block;
                width: 10px;
                height: 10px;
                background: #00ff96;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 1.5s infinite;
            }

            @keyframes pulse {
                0%   { box-shadow: 0 0 0 0 rgba(0,255,150,0.6); }
                70%  { box-shadow: 0 0 0 10px rgba(0,255,150,0); }
                100% { box-shadow: 0 0 0 0 rgba(0,255,150,0); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="badge">🚀 Live Deployment</div>
            <h1>GitOps Pipeline</h1>
            <p>
                <span class="pulse"></span>
                Successfully deployed via Jenkins & ArgoCD on Amazon EKS
            </p>
            <div class="stack">
                <span class="tag tag-blue">⚙️ Jenkins</span>
                <span class="tag tag-green">☸️ Kubernetes</span>
                <span class="tag tag-orange">🐳 Docker</span>
                <span class="tag tag-pink">🔄 ArgoCD</span>
                <span class="tag tag-purple">☁️ AWS EKS</span>
            </div>
            <div class="version">Built by Khaled Shawky · v4</div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)