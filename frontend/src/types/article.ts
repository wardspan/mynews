export interface ArticleBase {
    title: string;
    source: string;
    source_url: string;
    author?: string;
    published_date: string | Date;
    synopsis?: string;
    content?: string;
    image_url?: string;
    categories: string[];
    ai_tags?: string[];
  }
  
  export interface Article extends ArticleBase {
    id: string;
    created_at: string | Date;
    updated_at: string | Date;
  }
  
  export interface ArticleCreate extends ArticleBase {}
  
  export interface ArticleUpdate {
    title?: string;
    source?: string;
    source_url?: string;
    author?: string;
    published_date?: string | Date;
    synopsis?: string;
    content?: string;
    image_url?: string;
    categories?: string[];
    ai_tags?: string[];
  }
  
  export interface CategoryInfo {
    id: string;
    name: string;
    sources: string[];
  }
  
  export interface SourceInfo {
    id: string;
    name: string;
    enabled: boolean;
    description: string;
    categories: string[];
  }