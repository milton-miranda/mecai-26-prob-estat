def join_tabs (self):
    df = self \
        .merge(self, on="left") \
        .merge(self, on="left") \    
        .merge(self, on="left") \
        .merge(self, on="left")
        
    return df