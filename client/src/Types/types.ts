export interface Player {
  id: number;
  name: string;
  original_exp: number;
  created_at: Date;
}

export interface Hiscore {
  id: number;
  new_exp: number;
  total_gained_exp: number;
  created_at: Date;
  player_id: number;
}

export interface HiscoresByPlayer {
  player: Player;
  hiscores: Hiscore[];
}
