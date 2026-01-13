# Windows環境でのトラブルシューティング

このドキュメントでは、Windows環境でHorloqを使用する際によくある問題と解決方法を説明します。

## プラグインの依存関係インストール問題

### 問題1: 権限エラー（Permission Error）

**症状:**
```
ERROR: Could not install packages due to an OSError: [WinError 5] アクセスが拒否されました。
```

**解決方法:**

#### 方法A: --user オプションを使用（推奨）
```cmd
python -m pip install --user pynput
python -m pip install --user requests
```

#### 方法B: 管理者権限でコマンドプロンプトを実行
1. スタートメニューで「cmd」を検索
2. 右クリックして「管理者として実行」を選択
3. プラグインディレクトリに移動して依存関係をインストール:
```cmd
cd %USERPROFILE%\.horloq\plugins\bongocat
python -m pip install -r requirements.txt
```

### 問題2: pynputのインストールエラー

**症状:**
```
Building wheel for pynput (setup.py) ... error
```

**原因:**
pynputはネイティブコンポーネントを含むため、コンパイラが必要な場合があります。

**解決方法:**

#### 方法A: 事前ビルド版をインストール
```cmd
python -m pip install --upgrade pip
python -m pip install pynput --only-binary :all:
```

#### 方法B: Microsoft C++ Build Toolsをインストール
1. [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)をダウンロード
2. インストーラーで「C++ によるデスクトップ開発」を選択
3. 再度pynputをインストール:
```cmd
python -m pip install pynput
```

### 問題3: Python が見つからない

**症状:**
```
'python' は、内部コマンドまたは外部コマンド、
操作可能なプログラムまたはバッチ ファイルとして認識されていません。
```

**解決方法:**

#### 確認: Pythonがインストールされているか
```cmd
py --version
```

#### PATHへの追加:
1. 「システム環境変数の編集」を開く
2. 「環境変数」→「Path」を編集
3. 以下を追加:
   - `C:\Users\<ユーザー名>\AppData\Local\Programs\Python\Python311`
   - `C:\Users\<ユーザー名>\AppData\Local\Programs\Python\Python311\Scripts`

#### または Python Launcher を使用:
```cmd
py -m pip install pynput
```

### 問題4: 文字エンコーディングエラー

**症状:**
```
UnicodeDecodeError: 'cp932' codec can't decode byte...
```

**解決方法:**

環境変数を設定:
```cmd
set PYTHONIOENCODING=utf-8
python -m horloq
```

または、コマンドプロンプトのコードページを変更:
```cmd
chcp 65001
```

## バイナリ版での問題

### 問題: バイナリ版でプラグインの依存関係がインストールできない

**原因:**
バイナリ版（.exe）には埋め込みのPythonが使用されており、pipが含まれていません。

**解決方法:**

#### 方法A: システムのPythonを使用
1. Python 3.11以降をインストール: https://www.python.org/downloads/
2. 依存関係を手動でインストール:
```cmd
python -m pip install pynput requests
```

#### 方法B: ソースから実行
```cmd
git clone https://github.com/Nyayuta1060/Horloq.git
cd Horloq
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m horloq
```

## よくある質問

### Q: プラグインをインストールするたびにエラーが出る

**A:** 以下を確認してください：
1. Pythonが最新版か（3.11以降推奨）
2. pipが最新版か: `python -m pip install --upgrade pip`
3. 十分なディスク容量があるか
4. ウイルス対策ソフトがpipをブロックしていないか

### Q: Bongocat プラグインが動かない

**A:** pynputの初回起動時には管理者権限が必要な場合があります：
1. Horloqを管理者として実行
2. Bongocatプラグインを有効化
3. 次回以降は通常の権限で動作するはずです

### Q: Weather プラグインのAPIキーが保存されない

**A:** 設定ファイルへの書き込み権限を確認してください：
```cmd
icacls %USERPROFILE%\.horloq\plugins\weather\config.yaml
```

権限が不足している場合:
```cmd
icacls %USERPROFILE%\.horloq /grant %USERNAME%:(OI)(CI)F /T
```

## 報告とサポート

上記の解決方法で問題が解決しない場合は、以下の情報を添えてGitHub Issuesに報告してください：

1. Windows のバージョン（例: Windows 11 22H2）
2. Python のバージョン: `python --version`
3. エラーメッセージ全文
4. インストールしようとしたプラグイン名
5. バイナリ版かソース版か

GitHub Issues: https://github.com/Nyayuta1060/Horloq/issues
