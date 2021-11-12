# pydock

## pullrequest check

## remote-branch check 

## ブランチのテスト
- 特定のリモートブランチを取得する手順
1. git fetch で追跡ブランチを最新の状態にする
2. git checkout 作業したいブランチ で作業したいブランチに移動
2. もしくは, git checkout -b 作業したいブランチ 作業元のブランチ で作業したいブランチを作成&移動
3. git merge origin/取得したいリモートブランチ (つまり追跡ブランチをマージしている)


4. 取得した後に追加しているコメント