import bpy
import os
from datetime import datetime

def prompt_user_for_save_path():
    print("Prompting user for file save location and name...")
    bpy.ops.wm.save_as_mainfile('INVOKE_DEFAULT')

def save_blender_file(self, context):
    if bpy.data.filepath == "":
        print("No file path set, prompting user to save the file for the first time...")
        prompt_user_for_save_path()
        return {'CANCELLED'}
    else:
        main_file_path = bpy.data.filepath
        print(f"File already saved at: {main_file_path}")
        setup_wip_structure_and_save_wip(main_file_path)
        print(f"Reopening the main file: {main_file_path}")
        bpy.ops.wm.open_mainfile(filepath=main_file_path)
        return {'FINISHED'}

def setup_wip_structure_and_save_wip(main_file_path):
    folder_path = os.path.dirname(main_file_path)
    file_name = os.path.basename(main_file_path).replace(".blend", "")
    print(f"Setting up WIP structure in: {folder_path}")
    wip_folder = os.path.join(folder_path, "Wip")
    if not os.path.exists(wip_folder):
        os.makedirs(wip_folder)
        print(f"Created WIP folder: {wip_folder}")
    else:
        print(f"WIP folder already exists: {wip_folder}")
    save_wip_file(file_name, wip_folder)

def save_wip_file(file_name, wip_folder):
    timestamp = datetime.now().strftime("%m_%d_%y_%H_%M")
    wip_file_name = f"{file_name}_{timestamp}.blend"
    wip_file_path = os.path.join(wip_folder, wip_file_name)
    print(f"Saving WIP file: {wip_file_path}")
    bpy.ops.wm.save_as_mainfile(filepath=wip_file_path)
    print(f"WIP file saved: {wip_file_path}")

class CUSTOM_PT_AutoSavePanel(bpy.types.Panel):
    bl_label = "Auto Save"
    bl_idname = "CUSTOM_PT_auto_save_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Auto Save"
    def draw(self, context):
        layout = self.layout
        layout.operator("wm.auto_save", text="Save Now")

class WM_OT_AutoSave(bpy.types.Operator):
    bl_label = "Auto Save"
    bl_idname = "wm.auto_save"
    def execute(self, context):
        result = save_blender_file(self, context)
        return result

addon_keymaps = []

def register_hotkey():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(WM_OT_AutoSave.bl_idname, 'BUTTON4MOUSE', 'PRESS')
        addon_keymaps.append((km, kmi))
        print("Hotkey registered: Mouse Button 4")

def unregister_hotkey():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    print("Hotkey unregistered")

def register():
    bpy.utils.register_class(CUSTOM_PT_AutoSavePanel)
    bpy.utils.register_class(WM_OT_AutoSave)
    register_hotkey()
    print("Auto Save Panel registered")

def unregister():
    unregister_hotkey()
    bpy.utils.unregister_class(CUSTOM_PT_AutoSavePanel)
    bpy.utils.unregister_class(WM_OT_AutoSave)
    print("Auto Save Panel unregistered")

if __name__ == "__main__":
    register()
