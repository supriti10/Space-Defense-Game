import pygame

class Animation:
    def __init__(self, file_path, x, y, duration=1.0, scale=1.0):
        # Load the GIF as a sprite sheet
        self.sprite_sheet = pygame.image.load(file_path)
        
        # Get the dimensions of the entire sprite sheet
        self.sheet_width = self.sprite_sheet.get_width()
        self.sheet_height = self.sprite_sheet.get_height()
        
        # For simplicity, assume each frame is square and has the same size
        self.num_frames = self.sheet_width // self.sheet_height
        self.frame_width = self.sheet_height
        self.frame_height = self.sheet_height
        
        # Animation properties
        self.x = x
        self.y = y
        self.scale = scale
        self.current_frame = 0
        self.duration = duration  # Animation duration in seconds
        self.time_per_frame = duration / self.num_frames  # Time each frame should be displayed
        self.time_counter = 0
        self.completed = False
        
        # Extract frames
        self.frames = []
        for i in range(self.num_frames):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), 
                      (i * self.frame_width, 0, self.frame_width, self.frame_height))
            
            # Scale the frame if needed
            if scale != 1.0:
                new_width = int(self.frame_width * scale)
                new_height = int(self.frame_height * scale)
                frame = pygame.transform.scale(frame, (new_width, new_height))
            
            self.frames.append(frame)
    
    def update(self):
        if self.completed:
            return
            
        # Get time passed in this frame (assuming 60 FPS)
        frame_time = 1/60
        self.time_counter += frame_time
        
        # Calculate which frame to show based on elapsed time
        frame_index = int(self.time_counter / self.time_per_frame)
        
        # Update current frame
        if frame_index >= len(self.frames):
            self.completed = True
            self.current_frame = len(self.frames) - 1  # Stay on last frame
        else:
            self.current_frame = frame_index
    
    def draw(self, screen):
        if not self.completed or self.current_frame < len(self.frames):
            current_frame_img = self.frames[self.current_frame]
            screen.blit(current_frame_img, 
                      (self.x - current_frame_img.get_width() // 2, 
                       self.y - current_frame_img.get_height() // 2))
    
    def is_completed(self):
        return self.completed